import connexion
import six

from swagger_server.models.async_operation import AsyncOperation  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.last_operation_resource import LastOperationResource  # noqa: E501
from swagger_server.models.service_instance_async_operation import ServiceInstanceAsyncOperation  # noqa: E501
from swagger_server.models.service_instance_provision_request import ServiceInstanceProvisionRequest  # noqa: E501
from swagger_server.models.service_instance_provision_response import ServiceInstanceProvisionResponse  # noqa: E501
from swagger_server.models.service_instance_resource import ServiceInstanceResource  # noqa: E501
from swagger_server.models.service_instance_update_request import ServiceInstanceUpdateRequest  # noqa: E501
from swagger_server import util


def service_instance_deprovision(X_Broker_API_Version, service_id, plan_id, X_Broker_API_Originating_Identity=None, X_Broker_API_Request_Identity=None, accepts_incomplete=None):  # noqa: E501
    """deprovision a service instance

     # noqa: E501

    :param X_Broker_API_Version: version number of the Service Broker API that the Platform will use
    :type X_Broker_API_Version: str
    :param service_id: id of the service associated with the instance being deleted
    :type service_id: str
    :param plan_id: id of the plan associated with the instance being deleted
    :type plan_id: str
    :param X_Broker_API_Originating_Identity: identity of the user that initiated the request from the Platform
    :type X_Broker_API_Originating_Identity: str
    :param X_Broker_API_Request_Identity: idenity of the request from the Platform
    :type X_Broker_API_Request_Identity: str
    :param accepts_incomplete: asynchronous operations supported
    :type accepts_incomplete: bool

    :rtype: object
    """
    return 'do some magic!'


def service_instance_get(X_Broker_API_Version, X_Broker_API_Originating_Identity=None, X_Broker_API_Request_Identity=None, service_id=None, plan_id=None):  # noqa: E501
    """gets a service instance

     # noqa: E501

    :param X_Broker_API_Version: version number of the Service Broker API that the Platform will use
    :type X_Broker_API_Version: str
    :param X_Broker_API_Originating_Identity: identity of the user that initiated the request from the Platform
    :type X_Broker_API_Originating_Identity: str
    :param X_Broker_API_Request_Identity: idenity of the request from the Platform
    :type X_Broker_API_Request_Identity: str
    :param service_id: id of the service associated with the instance
    :type service_id: str
    :param plan_id: id of the plan associated with the instance
    :type plan_id: str

    :rtype: ServiceInstanceResource
    """
    return 'do some magic!'


def service_instance_last_operation_get(X_Broker_API_Version, X_Broker_API_Originating_Identity=None, X_Broker_API_Request_Identity=None, service_id=None, plan_id=None, operation=None):  # noqa: E501
    """last requested operation state for service instance

     # noqa: E501

    :param X_Broker_API_Version: version number of the Service Broker API that the Platform will use
    :type X_Broker_API_Version: str
    :param X_Broker_API_Originating_Identity: identity of the user that initiated the request from the Platform
    :type X_Broker_API_Originating_Identity: str
    :param X_Broker_API_Request_Identity: idenity of the request from the Platform
    :type X_Broker_API_Request_Identity: str
    :param service_id: id of the service associated with the instance
    :type service_id: str
    :param plan_id: id of the plan associated with the instance
    :type plan_id: str
    :param operation: a provided identifier for the operation
    :type operation: str

    :rtype: LastOperationResource
    """
    return 'do some magic!'


def service_instance_provision(X_Broker_API_Version, body, X_Broker_API_Originating_Identity=None, X_Broker_API_Request_Identity=None, accepts_incomplete=None):  # noqa: E501
    """provision a service instance

     # noqa: E501

    :param X_Broker_API_Version: version number of the Service Broker API that the Platform will use
    :type X_Broker_API_Version: str
    :param body: parameters for the requested service instance provision
    :type body: dict | bytes
    :param X_Broker_API_Originating_Identity: identity of the user that initiated the request from the Platform
    :type X_Broker_API_Originating_Identity: str
    :param X_Broker_API_Request_Identity: idenity of the request from the Platform
    :type X_Broker_API_Request_Identity: str
    :param accepts_incomplete: asynchronous operations supported
    :type accepts_incomplete: bool

    :rtype: ServiceInstanceProvisionResponse
    """
    if connexion.request.is_json:
        body = ServiceInstanceProvisionRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def service_instance_update(X_Broker_API_Version, body, X_Broker_API_Originating_Identity=None, X_Broker_API_Request_Identity=None, accepts_incomplete=None):  # noqa: E501
    """update a service instance

     # noqa: E501

    :param X_Broker_API_Version: version number of the Service Broker API that the Platform will use
    :type X_Broker_API_Version: str
    :param body: parameters for the requested service instance update
    :type body: dict | bytes
    :param X_Broker_API_Originating_Identity: identity of the user that initiated the request from the Platform
    :type X_Broker_API_Originating_Identity: str
    :param X_Broker_API_Request_Identity: idenity of the request from the Platform
    :type X_Broker_API_Request_Identity: str
    :param accepts_incomplete: asynchronous operations supported
    :type accepts_incomplete: bool

    :rtype: object
    """
    if connexion.request.is_json:
        body = ServiceInstanceUpdateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
