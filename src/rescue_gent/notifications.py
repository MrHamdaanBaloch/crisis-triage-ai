import requests
import os

def send_slack_alert(priority_score: int, message: str, needs: list, incident_id: int):
    """Sends a formatted, actionable alert to a Slack channel."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("WARNING: SLACK_WEBHOOK_URL not found in .env file. Skipping alert.")
        return

    needs_str = ", ".join(needs) if needs else "Not specified"
    alert_blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"🚨 High-Priority Incident #{incident_id}", "emoji": True}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*Priority Score:*\n*{priority_score}/100*"},
            {"type": "mrkdwn", "text": f"*Resource Needs:*\n{needs_str}"}
        ]},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Original Report:*\n```{message}```"}},
        {"type": "divider"}
    ]
    payload = {"blocks": alert_blocks}
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Slack alert for incident #{incident_id} sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to send Slack alert: {e}")