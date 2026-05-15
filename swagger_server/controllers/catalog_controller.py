import connexion  # pyright: ignore[reportMissingImports]
import six

from swagger_server.models.catalog import Catalog  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.plan import Plan  # noqa: E501
from swagger_server.models.service import Service  # noqa: E501
from swagger_server import util


SERVICE_ID = "be0e6c99-d3e5-4696-8835-917bd718fb84"
SERVICE_NAME = "mylua-health-inc-mylua-care-recommendation-agent"
SERVICE_DESCRIPTION = (
    "A maternal care clinical support agent that analyzes patient documents, "
    "notes, and questions to recommend structured, evidence-informed care "
    "pathways for clinicians and care teams."
)


def _plan(id, name, display_name, description, monthly_price, case_price, included_cases):
    return Plan(
        id=id,
        name=name,
        description=description,
        metadata={
            "displayName": display_name,
            "bullets": [
                "Usage-based pricing",
                "Annual commitment, billed monthly",
                f"Up to {included_cases:,} member records analyzed per month",
                f"${case_price:g} per case analysis over cap",
            ],
            "costs": [
                {
                    "amount": {"usd": monthly_price},
                    "unit": "MONTHLY",
                },
                {
                    "amount": {"usd": case_price},
                    "unit": "MYLUA_CASE_ANALYSIS",
                },
            ],
        },
        free=False,
        bindable=False,
        plan_updateable=True,
    )


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
            id=SERVICE_ID,
            name=SERVICE_NAME,
            description=SERVICE_DESCRIPTION,
            bindable=False,
            instances_retrievable=True,
            allow_context_updates=True,
            plan_updateable=True,
            plans=[
                _plan(
                    id="9642aa35-837e-4589-adfc-c29cad295004",
                    name="standard",
                    display_name="Standard",
                    description=(
                        "For care coordination organizations, community health programs, "
                        "and employer pilot initiatives. Up to 500 case analyses per month. "
                        "$11 per case over cap. Annual commitment, billed monthly."
                    ),
                    monthly_price=1800,
                    case_price=11,
                    included_cases=500,
                ),
                _plan(
                    id="e1feb0c7-a004-481c-9326-066884b9e6ed",
                    name="professional",
                    display_name="Professional",
                    description=(
                        "For health plans, employer health programs, and regional care "
                        "management teams. Up to 2,000 case analyses per month. $6 per "
                        "case over cap. Annual commitment, billed monthly."
                    ),
                    monthly_price=6000,
                    case_price=6,
                    included_cases=2000,
                ),
                _plan(
                    id="42ff6325-4507-4aba-9b89-d78ddd67fab7",
                    name="enterprise",
                    display_name="Enterprise",
                    description=(
                        "For national health plans, large MCOs, and enterprise employer "
                        "maternal health programs. Up to 10,000 case analyses per month. "
                        "$4 per case over cap. Annual commitment, billed monthly."
                    ),
                    monthly_price=18000,
                    case_price=4,
                    included_cases=10000,
                ),
            ],
        )
    ])
