import os

import connexion
import psycopg2
from psycopg2.extras import Json, RealDictCursor

from swagger_server.models.error import Error
from swagger_server.models.last_operation_resource import LastOperationResource
from swagger_server.models.service_instance_resource import ServiceInstanceResource

SERVICE_ID = "be0e6c99-d3e5-4696-8835-917bd718fb84"
PLAN_ID = "9642aa35-837e-4589-adfc-c29cad295004"
PLAN_IDS = {
    "9642aa35-837e-4589-adfc-c29cad295004",
    "e1feb0c7-a004-481c-9326-066884b9e6ed",
    "42ff6325-4507-4aba-9b89-d78ddd67fab7",
}
DASHBOARD_URL = "https://www.myluahealth.com/"


def _db_config():
    return {
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT", "5432"),
        "dbname": os.environ.get("DB_DATABASE"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
    }


def _db_enabled():
    config = _db_config()
    return all(config.get(key) for key in ("host", "dbname", "user", "password"))


def _connect_db():
    return psycopg2.connect(**_db_config())


def _error(status_code, error, description):
    return Error(error=error, description=description), status_code


def _request_body():
    return connexion.request.get_json(silent=True) or {}


def _validate_service_plan(service_id, plan_id):
    if service_id != SERVICE_ID:
        return _error(
            422,
            "InvalidServiceId",
            "The requested service_id does not match this broker catalog.",
        )

    if plan_id not in PLAN_IDS:
        return _error(
            422,
            "InvalidPlanId",
            "The requested plan_id does not match this broker catalog.",
        )

    return None


def _context_from_body(body):
    context = body.get("context") or {}
    return {
        "account_id": context.get("account_id", ""),
        "crn": context.get("crn", ""),
        "resource_group_crn": context.get("resource_group_crn", ""),
        "platform": context.get("platform", ""),
    }


def _metadata(body=None):
    body = body or {}
    return {
        "labels": {
            "service_id": body.get("service_id", SERVICE_ID),
            "plan_id": body.get("plan_id", PLAN_ID),
        },
        "attributes": {
            "provisioned_by": "mylua-care-broker",
            "lifecycle": "native-agent-noop",
        },
        "context": _context_from_body(body),
    }


def _upsert_instance(instance_id, service_id, plan_id, context, parameters):
    if not _db_enabled():
        return

    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ibm_service_instances (
                    instance_id,
                    resource_instance_crn,
                    account_id,
                    resource_group_crn,
                    service_id,
                    plan_id,
                    status,
                    context_json,
                    parameters_json,
                    updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, 'active', %s, %s, NOW())
                ON CONFLICT (instance_id) DO UPDATE SET
                    resource_instance_crn = EXCLUDED.resource_instance_crn,
                    account_id = EXCLUDED.account_id,
                    resource_group_crn = EXCLUDED.resource_group_crn,
                    service_id = EXCLUDED.service_id,
                    plan_id = EXCLUDED.plan_id,
                    status = 'active',
                    context_json = EXCLUDED.context_json,
                    parameters_json = EXCLUDED.parameters_json,
                    updated_at = NOW()
                """,
                (
                    instance_id,
                    context.get("crn", ""),
                    context.get("account_id", ""),
                    context.get("resource_group_crn", ""),
                    service_id,
                    plan_id,
                    Json(context),
                    Json(parameters or {}),
                ),
            )


def _get_instance(instance_id):
    if not _db_enabled():
        return None

    with _connect_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    instance_id,
                    resource_instance_crn,
                    account_id,
                    resource_group_crn,
                    service_id,
                    plan_id,
                    status,
                    context_json,
                    parameters_json
                FROM ibm_service_instances
                WHERE instance_id = %s
                """,
                (instance_id,),
            )
            return cur.fetchone()


def _mark_deprovisioned(instance_id):
    if not _db_enabled():
        return

    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE ibm_service_instances
                SET status = 'deprovisioned', updated_at = NOW()
                WHERE instance_id = %s
                """,
                (instance_id,),
            )


def service_instance_deprovision(**kwargs):
    instance_id = kwargs.get("instance_id")
    service_id = kwargs.get("service_id")
    plan_id = kwargs.get("plan_id")

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    _mark_deprovisioned(instance_id)
    return {}, 200


def service_instance_get(**kwargs):
    instance_id = kwargs.get("instance_id")
    service_id = kwargs.get("service_id") or SERVICE_ID
    plan_id = kwargs.get("plan_id") or PLAN_ID

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    record = _get_instance(instance_id)
    status = record.get("status") if record else "active"

    return ServiceInstanceResource(
        service_id=service_id,
        plan_id=plan_id,
        dashboard_url=DASHBOARD_URL,
        parameters={"status": status, "lifecycle": "native-agent-noop"},
    )


def service_instance_last_operation_get(**kwargs):
    return LastOperationResource(
        state="succeeded",
        description="Native agent lifecycle operation completed successfully.",
        instance_usable=True,
        update_repeatable=True,
    )


def service_instance_provision(**kwargs):
    instance_id = kwargs.get("instance_id")
    body = _request_body()
    service_id = body.get("service_id", SERVICE_ID)
    plan_id = body.get("plan_id", PLAN_ID)

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    context = _context_from_body(body)
    parameters = body.get("parameters") or {}
    _upsert_instance(instance_id, service_id, plan_id, context, parameters)

    return {
        "dashboard_url": DASHBOARD_URL,
        "metadata": _metadata(body),
    }, 201


def service_instance_update(**kwargs):
    instance_id = kwargs.get("instance_id")
    body = _request_body()
    service_id = body.get("service_id", SERVICE_ID)
    plan_id = body.get("plan_id", PLAN_ID)

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    context = _context_from_body(body)
    parameters = body.get("parameters") or {}
    _upsert_instance(instance_id, service_id, plan_id, context, parameters)

    return {}, 200
