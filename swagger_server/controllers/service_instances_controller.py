import connexion

from swagger_server.models.error import Error
from swagger_server.models.last_operation_resource import LastOperationResource
from swagger_server.models.service_instance_resource import ServiceInstanceResource

SERVICE_ID = "be0e6c99-d3e5-4696-8835-917bd718fb84"
PLAN_ID = "9642aa35-837e-4589-adfc-c29cad295004"
DASHBOARD_URL = "https://www.myluahealth.com/"


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

    if plan_id != PLAN_ID:
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


def service_instance_deprovision(**kwargs):
    service_id = kwargs.get("service_id")
    plan_id = kwargs.get("plan_id")

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    return {}, 200


def service_instance_get(**kwargs):
    service_id = kwargs.get("service_id") or SERVICE_ID
    plan_id = kwargs.get("plan_id") or PLAN_ID

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    return ServiceInstanceResource(
        service_id=service_id,
        plan_id=plan_id,
        dashboard_url=DASHBOARD_URL,
        parameters={"status": "active", "lifecycle": "native-agent-noop"},
    )


def service_instance_last_operation_get(**kwargs):
    return LastOperationResource(
        state="succeeded",
        description="Native agent lifecycle operation completed successfully.",
        instance_usable=True,
        update_repeatable=True,
    )


def service_instance_provision(**kwargs):
    body = _request_body()
    service_id = body.get("service_id", SERVICE_ID)
    plan_id = body.get("plan_id", PLAN_ID)

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    return {
        "dashboard_url": DASHBOARD_URL,
        "metadata": _metadata(body),
    }, 201


def service_instance_update(**kwargs):
    body = _request_body()
    service_id = body.get("service_id", SERVICE_ID)
    plan_id = body.get("plan_id", PLAN_ID)

    validation_error = _validate_service_plan(service_id, plan_id)
    if validation_error:
        return validation_error

    return {}, 200
