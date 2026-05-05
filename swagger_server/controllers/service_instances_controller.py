import connexion

from swagger_server.models.last_operation_resource import LastOperationResource  # noqa: E501
from swagger_server.models.service_instance_resource import ServiceInstanceResource  # noqa: E501


DEMO_SERVICE_ID = "open-service-broker-demo-service"
DEMO_PLAN_ID = "open-service-broker-demo-plan"


def _instance_payload(service_id=None, plan_id=None):
    return ServiceInstanceResource(
        service_id=service_id or DEMO_SERVICE_ID,
        plan_id=plan_id or DEMO_PLAN_ID,
        dashboard_url="https://example.com/dashboard/demo-instance",
        parameters={"status": "active"},
    )


def service_instance_deprovision(**kwargs):  # noqa: E501
    """deprovision a service instance"""
    return {}, 200


def service_instance_get(**kwargs):  # noqa: E501
    """gets a service instance"""
    return _instance_payload(
        service_id=kwargs.get("service_id"),
        plan_id=kwargs.get("plan_id"),
    )


def service_instance_last_operation_get(**kwargs):  # noqa: E501
    """last requested operation state for service instance"""
    return LastOperationResource(
        state="succeeded",
        description="Last requested operation completed successfully.",
        instance_usable=True,
        update_repeatable=True,
    )


def service_instance_provision(**kwargs):  # noqa: E501
    """provision a service instance"""
    body = connexion.request.get_json(silent=True) or {}
    return {
        "dashboard_url": "https://example.com/dashboard/demo-instance",
        "metadata": {
            "labels": {
                "service_id": body.get("service_id", DEMO_SERVICE_ID),
                "plan_id": body.get("plan_id", DEMO_PLAN_ID),
            },
            "attributes": {
                "provisioned_by": "demo-broker",
            },
        },
    }, 201


def service_instance_update(**kwargs):  # noqa: E501
    """update a service instance"""
    return {}, 200
