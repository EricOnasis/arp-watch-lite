"""Minimal webhook notifications: generic/Slack/Discord/ntfy."""
import json
from urllib import error, request


def send_webhook(url: str, webhook_type: str, message: str) -> None:
    try:
        if webhook_type == "slack":
            body = json.dumps({"text": message}).encode("utf-8")
            headers = {"Content-Type": "application/json"}
        elif webhook_type == "discord":
            body = json.dumps({"content": message}).encode("utf-8")
            headers = {"Content-Type": "application/json"}
        elif webhook_type == "ntfy":
            body = message.encode("utf-8")
            headers = {"Content-Type": "text/plain; charset=utf-8"}
        else:  # generic
            body = json.dumps({"text": message}).encode("utf-8")
            headers = {"Content-Type": "application/json"}

        req = request.Request(url, data=body, headers=headers, method="POST")
        with request.urlopen(req, timeout=10) as resp:
            resp.read()
    except error.URLError as e:
        print(f"Failed to send webhook notification: {e}")
