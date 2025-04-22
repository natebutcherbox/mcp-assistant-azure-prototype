import json
import logging
from fastmcp import FastMCP

# Set up logging with more granularity
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger("data_server")
# Ensure FastMCP internal logs are captured
fastmcp_logger = logging.getLogger("mcp.server")
fastmcp_logger.setLevel(logging.DEBUG)

# Create the FastMCP server
data_mcp = FastMCP("System Data Server")

# Define company acronyms dictionary
COMPANY_ACRONYMS = {
    "A&E": "Activate and Engage - two metrics that we measure to track whether members have increased their spend with us via an upgrade or deal/addon (Activation), and if they are regularly interacting with us via the website, filling out surveys, etc. (Engagement)",
    "AOV": "Average Order Value",
    "API": "Application Programming interface — a set of functions and procedures allowing the creation of technical applications that access the features or data of a web system or other service.",
    "APIv4": "Version 4 of Butcherbox Engineering API service. Provides website data and functionality to butcherbox.com.",
    "BFCM": "Black Friday Cyber Monday",
    "BDM": "Bill Date Movement",
    "BMC": "Business Model Canvas",
    "CAPI": "Facebook Conversions API",
    "CCI": "Consumer Confidence Index",
    "CDP": "Customer Data Platform",
    "CMS": "Content Management System (we use Contentful)",
    "COE": "Center Of Excellence",
    "COGS": "Cost Of Goods Sold",
    "CPA": "Cost Per Acquisition",
    "CPL": "Cost Per Purchase",
    "CPP": "Cron Process Payments (replaced by ProcessPaymentsJob; CPP → CTUP → DOM)",
    "CRM": "Customer Relationship Management (system to track customer information and activity, we especially leverage these for corporate clients)",
    "CRO": "Conversion Rate Optimization",
    "CSAT": "Customer Satisfaction",
    "CSE": "Customer Support Experience",
    "CSP": "Customer Support Portal",
    "CTR": "Click Through Rate",
    "CTUP": "Cron Transfer Up - a process that sends orders to the DOM (replaced by SendOrdersToFulfillmentJob; CPP → CTUP → DOM)",
    "CVR": "ConVersion Rate",
    "DAM": "Digital Asset Management (Creative/Audio Visual world)",
    "DC/FC/Warehouse": "Order Fulfillment Distribution Warehouse",
    "DOM": "Delivery Order Management system (Payment → Box on Customer's Doorstep)",
    "DSAR": "Data Subject Access Request. A request submitted by individuals to businesses asking what personal data of theirs is gathered and used by the company. Also, other privacy protection requests such as 'do not track and 'do not profile' restrictions may be referred to. Important for complying with international data privacy legislation such as GDPR and CCPA.",
    "DSAT": "Delivery Satisfaction. A survey is sent to customers after their box is delivered.",
    "DTC": "Direct to Consumer",
    "ERD": "Entity relationship diagram",
    "ERP": "Enterprise Resource Planning is software that organizations use to manage day-to-day business activities such as accounting, procurement, project management, risk management and compliance, and supply chain operations.",
    "FTP": "At ButcherBox, FTP does not translate to 'file transfer protocol' but simply refers to orders.",
    "FSQS": "Food Science Quality and Safety",
    "GA": "Google Analytics",
    "GBB": "Good, Better, Best",
    "GM": "Gross Margin",
    "GP$": "Gross Profit",
    "IDM": "Identity Access Management",
    "K8/K8S/AKS": "Kubernetes - open-source system for automating deployment, scaling, and managing containerized applications. AKS is Azure Kubernetes Service - Azure's k8s PaaS technology for running k8s clusters with the master backplane nodes managed by Azure (easier to operate and maintain).",
    "KLTO": "Keep the LighTs On",
    "LTV": "Life Time Value",
    "MDW": "Memorial Day Weekend",
    "MMP": "Module Marketing Product (i.e. Contentful module to fetch Shopify Products)",
    "MSAL": "Microsoft Authentication Library",
    "MSAT": "Member Satisfaction",
    "NPS": "Net Promoter Score (measurement that aims to quantify brand loyalty)",
    "NRR": "Net Revenue Retention",
    "OMM": "Orders per Member per Month",
    "O&D": "Order & Delivery Squad",
    "OKRs": "Objectives & Key Results",
    "OTB": "One Time Box",
    "P&D": "Process and Delivery Team",
    "PCI compliance": "Payment card industry (PCI) compliance is mandated by credit card companies to help ensure the security of credit card transactions",
    "PII": "Personally Identifiable Information (relates to data privacy)",
    "PIM": "Product Management System / Privileged Identity Management (relates to IT)",
    "PLP": "Products Listing Page",
    "PO": "Product Owner",
    "QBR": "Quarterly Business Review",
    "RACI": "Responsible, Accountable, Consulted, and Informed (a matrix of roles and responsibilities)",
    "PDP": "Product Details Page",
    "RFC": "Request For Comment (engineering document proposing a solution with request for review)",
    "SCO": "Supply Chain Ops",
    "SER": "Social and Environmental Responsibility",
    "SLA": "Service-Level Agreement (between a service provider and a client)",
    "SME": "Subject Matter Expert",
    "TBI": "Technical Backlog Item",
    "UTT": "Universal Tracking Tag",
    "WBR": "Weekly Business Review"
}

# Add a resource for company acronyms
@data_mcp.resource(
    uri="data://company-acronyms",
    name="CompanyAcronyms",
    description="Returns the company acronyms and their definitions",
    mime_type="application/json"
)
def get_company_acronyms() -> dict:
    """Returns the full list of company acronyms and their meanings."""
    logger.info("get_company_acronyms resource function called!")
    return COMPANY_ACRONYMS

# Add a resource to look up specific acronyms
@data_mcp.resource(
    uri="data://company-acronyms/{acronym}",
    name="AcronymLookup",
    description="Look up the definition of a specific company acronym",
    mime_type="application/json"
)
def get_acronym_definition(acronym: str) -> dict:
    logger.info(f"get_acronym_definition resource function called for: {acronym}")

    # Case-insensitive lookup
    for key, definition in COMPANY_ACRONYMS.items():
        if key.lower() == acronym.lower():
            return {
                "acronym": key,
                "definition": definition,
                "found": True
            }

    return {
        "acronym": acronym,
        "definition": "Acronym not found",
        "found": False
    }

# Add a tool function for looking up acronyms
@data_mcp.tool()
def lookup_company_acronym(acronym: str) -> dict:
    logger.info(f"lookup_company_acronym tool function called for: {acronym}")

    # Case-insensitive lookup
    for key, definition in COMPANY_ACRONYMS.items():
        if key.lower() == acronym.lower():
            return {
                "acronym": key,
                "definition": definition,
                "found": True
            }

    return {
        "acronym": acronym,
        "definition": "Acronym not found",
        "found": False
    }

# Add a tool function to get all acronyms
@data_mcp.tool()
def get_all_company_acronyms() -> dict:
    logger.info("get_all_company_acronyms tool function called!")
    return COMPANY_ACRONYMS

# Log what's been registered
logger.info("Registered MCP Resources:")
for uri in data_mcp._resource_manager.get_resources():
    logger.info(f" - {uri}")

logger.info("Registered MCP Tools:")
for tool in data_mcp._tool_manager.get_tools():
    logger.info(f" - {tool}")

if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description='Start the Data Server')
    parser.add_argument('--port', type=int, default=8002, help='Port to run the server on')
    args = parser.parse_args()

    logger.info(f"Starting System Data Server on http://127.0.0.1:{args.port}")
    asyncio.run(
        data_mcp.run_sse_async(
            host="127.0.0.1",
            port=args.port,
            log_level="debug"
        )
    )