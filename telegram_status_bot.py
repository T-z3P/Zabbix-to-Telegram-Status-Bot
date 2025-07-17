import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Configuration ---
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ZABBIX_URL = "http://127.0.0.1/zabbix/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASS = "your_admin_password"

# Severity mapping
SEVERITY_EMOJI = {
    "5": "🔥 Disaster",
    "4": "🔴 High",
    "3": "🔶 Average",
    "2": "⚠️ Warning",
    "1": "ℹ️ Information",
    "0": "🔘 Not classified"
}

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Zabbix API functions ---
def get_zabbix_auth():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login.password",
        "params": {
            "username": ZABBIX_USER,
            "password": ZABBIX_PASS
        },
        "id": 1
    }
    response = requests.post(ZABBIX_URL, json=payload)
    logger.debug("Zabbix login response: %s", response.text)
    data = response.json()

    if "error" in data:
        error_message = data["error"].get("data", "Unknown error")
        raise Exception(f"Zabbix login failed: {error_message}")

    return data["result"]

def get_problem_summary(auth_token):
    payload = {
        "jsonrpc": "2.0",
        "method": "problem.get",
        "params": {
            "output": ["severity"],
            "sortfield": "severity",
            "sortorder": "DESC"
        },
        "auth": auth_token,
        "id": 2
    }
    response = requests.post(ZABBIX_URL, json=payload)
    data = response.json()

    if "error" in data:
        error_message = data["error"].get("data", "Unknown error")
        raise Exception(f"Zabbix API error: {error_message}")

    counts = {k: 0 for k in SEVERITY_EMOJI.keys()}
    for problem in data["result"]:
        severity = problem["severity"]
        counts[severity] += 1

    return counts

# --- Telegram bot handlers ---
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        auth_token = get_zabbix_auth()
        summary = get_problem_summary(auth_token)

        message = "\ud83d\udcca *Zabbix Problem Summary by Severity:*\n"
        for severity in sorted(SEVERITY_EMOJI.keys(), key=int, reverse=True):
            label = SEVERITY_EMOJI[severity]
            count = summary.get(severity, 0)
            message += f"{label}: `{count}`\n"

        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        logger.error("Error handling /status command", exc_info=True)
        await update.message.reply_text(f"\u274c Error: {str(e)}")

# --- Main bot runner ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("status", status))
    app.run_polling()

if __name__ == "__main__":
    main()
