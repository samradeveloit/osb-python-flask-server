import connexion  # pyright: ignore[reportMissingImports]
import six

from swagger_server.models.catalog import Catalog  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.plan import Plan  # noqa: E501
from swagger_server.models.service import Service  # noqa: E501
from swagger_server import util


def catalog_get(**kwargs):  # noqa: E501
    """get the catalog of services that the service broker offers

     # noqa: E501

    :param X_Broker_API_Version: version number of the Service Broker API that the Platform will use
    :type X_Broker_API_Version: str
    :param X_Broker_API_Originating_Identity: identity of the user that initiated the request from the Platform
    :type X_Broker_API_Originating_Identity: str
    :param X_Broker_API_Request_Identity: idenity of the request from the Platform
    :type X_Broker_API_Request_Identity: str

    :rtype: Catalog
    """
    return Catalog(services=[
        Service(
            id='be0e6c99-d3e5-4696-8835-917bd718fb84',
            name='mylua-health-inc-mylua-care-recommendation-agent',
            description='A maternal care clinical support agent that analyzes patient documents, notes, and questions to recommend structured, evidence-informed care pathways for clinicians and care teams.',
            bindable=False,
            plan_updateable=False,
            plans=[
                Plan(
                    id='9642aa35-837e-4589-adfc-c29cad295004',
                    name='standard',
                    description='Standard plan with usage-based pricing for MyLUA Care Recommendation Agent',
                    free=False,
                )
            ],
        )
    ])
