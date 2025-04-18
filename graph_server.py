import os
import requests
from fastmcp import FastMCP
from msal import ConfidentialClientApplication
from datetime import timedelta
from dateutil import parser
import pytz

mcp = FastMCP("Graph Calendar Server")

def get_graph_token():
    app = ConfidentialClientApplication(
        os.environ["GRAPH_CLIENT_ID"],
        authority=f"https://login.microsoftonline.com/{os.environ['GRAPH_TENANT_ID']}",
        client_credential=os.environ["GRAPH_CLIENT_SECRET"]
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token["access_token"]

@mcp.tool()
def create_event(subject: str, attendees: list[str], start_time: str, duration: int) -> str:
    """Create a calendar event using Microsoft Graph API."""
    token = get_graph_token()

    # Parse the time with fallback to America/New_York
    try:
        start_dt = parser.parse(start_time)
        if start_dt.tzinfo is None:
            start_dt = pytz.timezone("America/New_York").localize(start_dt)
        start_dt_utc = start_dt.astimezone(pytz.utc)
    except Exception as e:
        return f"❌ Failed to parse date/time: {e}"

    end_dt_utc = start_dt_utc + timedelta(minutes=duration)

    event = {
        "subject": subject,
        "start": {
            "dateTime": start_dt_utc.isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_dt_utc.isoformat(),
            "timeZone": "UTC"
        },
        "attendees": [
            {"emailAddress": {"address": email}, "type": "required"}
            for email in attendees
        ]
    }

    res = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{os.environ['GRAPH_USER_EMAIL']}/events",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=event
    )

    if res.status_code == 201:
        return "📅 Meeting successfully scheduled."
    else:
        print("[error]", res.status_code, res.text)
        return "❌ Failed to schedule meeting."

if __name__ == "__main__":
    import asyncio
    asyncio.run(
        mcp.run_sse_async(
            host="127.0.0.1",
            port=8001,
            log_level="debug"
        )
    )
