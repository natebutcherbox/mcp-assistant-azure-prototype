import os
import requests
from fastmcp import FastMCP
from msal import ConfidentialClientApplication
from datetime import timedelta
from dateutil import parser
import pytz

mcp = FastMCP("Graph Online Meeting Server")

def get_graph_token():
    app = ConfidentialClientApplication(
        os.environ["GRAPH_CLIENT_ID"],
        authority=f"https://login.microsoftonline.com/{os.environ['GRAPH_TENANT_ID']}",
        client_credential=os.environ["GRAPH_CLIENT_SECRET"]
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token["access_token"]

@mcp.tool()
def create_online_meeting(subject: str, start_time: str, duration: int) -> str:
    """Create a Microsoft Teams online meeting using the Graph API."""
    token = get_graph_token()

    try:
        start_dt = parser.parse(start_time)
        if start_dt.tzinfo is None:
            start_dt = pytz.timezone("America/New_York").localize(start_dt)
        start_dt_utc = start_dt.astimezone(pytz.utc)
    except Exception as e:
        return f"Failed to parse date/time: {e}"

    end_dt_utc = start_dt_utc + timedelta(minutes=duration)

    meeting_data = {
        "startDateTime": start_dt_utc.isoformat(),
        "endDateTime": end_dt_utc.isoformat(),
        "subject": subject
    }

    response = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{os.environ['GRAPH_USER_ID']}/onlineMeetings",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=meeting_data
    )

    if response.status_code == 201:
        meeting = response.json()
        return f"Online meeting created: {meeting.get('joinWebUrl')}"
    else:
        print("[error]", response.status_code, response.text)
        return "Failed to create online meeting."

if __name__ == "__main__":
    import asyncio
    asyncio.run(
        mcp.run_sse_async(
            host="127.0.0.1",
            port=8001,
            log_level="debug"
        )
    )