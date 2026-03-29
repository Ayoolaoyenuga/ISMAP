"""
alerts.py - Multi-channel notification dispatch for ISMAP.
"""

import logging
import re
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText

import requests

logger = logging.getLogger(__name__)


def _clean_message_text(message: str) -> str:
    """Repair mojibake while keeping the original report-style layout."""
    if not message:
        return message

    cleaned = message
    replacements = {
        "Ã¢â‚¬Â¢": "•",
        "â€¢": "•",
        "Ã¢â€ â€™": "→",
        "â†’": "→",
        "Ã¢Å“â€¦": "✅",
        "âœ…": "✅",
        "Ã°Å¸Å¡â‚¬": "🚀",
        "ðŸš€": "🚀",
        "Ã°Å¸Å¡Â¨": "🚨",
        "ðŸš¨": "🚨",
        "âš ï¸": "⚠️",
        "ðŸ”„": "🔄",
    }
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    if "Initial scan for" in cleaned and "Discovered" in cleaned:
        first_line, _, rest = cleaned.partition("\n")
        match = re.search(r"Initial scan for \*(.+?)\* completed! Discovered (\d+) subdomains", first_line)
        if match:
            domain = match.group(1)
            count = match.group(2)
            bullet_lines = []
            for line in rest.splitlines():
                line = line.strip()
                if not line or line == "Subdomain List:":
                    continue
                if line.startswith("•") or line.startswith("..."):
                    if line.startswith("..."):
                        bullet_lines.append(f"• {line}")
                    else:
                        bullet_lines.append(line)
            rebuilt = [
                f"🚨 *ISMAP Scan Report for {domain}* 🚨",
                "",
                f"*Initial Scan Results ({count})*",
            ]
            rebuilt.extend(bullet_lines)
            rebuilt.append("")
            rebuilt.append(f"Total subdomains active: {count}")
            return "\n".join(rebuilt).strip()

    return cleaned


def send_slack_alert(message: str, webhook_url: str) -> dict:
    if not webhook_url:
        return {"success": False, "message": "Slack webhook is not configured."}
    try:
        resp = requests.post(webhook_url, json={"text": message}, timeout=5)
        resp.raise_for_status()
        logger.info("Slack alert sent successfully (status %d)", resp.status_code)
        return {"success": True, "message": "Slack alert sent successfully."}
    except Exception as exc:
        logger.error("Slack alert failed: %s", exc)
        return {"success": False, "message": f"Slack alert failed: {exc}"}


def send_telegram_alert(message: str, bot_token: str, chat_id: str) -> dict:
    if not bot_token or not chat_id:
        return {"success": False, "message": "Telegram bot token or chat ID is missing."}
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        resp = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message,
                "disable_web_page_preview": True,
            },
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            desc = data.get("description", "Unknown Telegram API error")
            logger.error("Telegram alert failed: %s", desc)
            return {"success": False, "message": f"Telegram alert failed: {desc}"}
        logger.info("Telegram alert sent successfully")
        return {"success": True, "message": "Telegram alert sent successfully."}
    except Exception as exc:
        logger.error("Telegram alert failed: %s", exc)
        return {"success": False, "message": f"Telegram alert failed: {exc}"}


def send_email_alert(
    subject: str,
    body: str,
    smtp_server: str,
    smtp_port: int,
    sender: str,
    password: str,
    recipient: str,
) -> dict:
    if not sender or not password or not recipient:
        return {"success": False, "message": "Email sender, password, or recipient is missing."}
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, [recipient], msg.as_string())
        logger.info("Email alert sent successfully")
        return {"success": True, "message": "Email alert sent successfully."}
    except Exception as exc:
        logger.error("Email alert failed: %s", exc)
        return {"success": False, "message": f"Email alert failed: {exc}"}


def send_alert(
    change_type: str,
    subdomain: str,
    domain: str,
    alert_config: dict,
    *,
    extra: str | None = None,
):
    """
    Dispatch an alert to all configured channels.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    message = extra or (
        f"ISMAP Alert: {change_type}\n\n"
        f"Domain: {domain}\nSubdomain: {subdomain}\nTime: {timestamp}"
    )
    message = _clean_message_text(message)

    results = {}

    if alert_config.get("slack_webhook"):
        results["slack"] = send_slack_alert(message, alert_config["slack_webhook"])

    if alert_config.get("telegram_bot_token") and alert_config.get("telegram_chat_id"):
        results["telegram"] = send_telegram_alert(
            message,
            alert_config["telegram_bot_token"],
            alert_config["telegram_chat_id"],
        )

    if alert_config.get("email"):
        results["email"] = send_email_alert(
            subject=f"ISMAP Alert: {change_type}",
            body=message,
            smtp_server=alert_config.get("smtp_server", "smtp.gmail.com"),
            smtp_port=alert_config.get("smtp_port", 587),
            sender=alert_config["email"],
            password=alert_config.get("email_password", ""),
            recipient=alert_config["email"],
        )

    return results
