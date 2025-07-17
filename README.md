# Zabbix-to-Telegram Status Bot
A simple Python bot that integrates with Zabbix and provides real-time `/status` reports via Telegram, showing the current count of problems grouped by severity (like the Zabbix dashboard).

---

## 📊 Example Output

📊 Zabbix Problem Summary by Severity:

🔥 Disaster: 0

🔴 High: 1

🔷 Average: 3

⚠️ Warning: 2

ℹ️ Information: 0

🔘 Not classified: 0

---

## 🚀 Features

- Telegram `/status` command
- Live Zabbix API integration
- Shows problems by severity
- Emoji-labeled and formatted for clarity
- Graceful error handling

---

## 🛠️ Requirements

- Python 3.8+
- Zabbix server with API access
- Telegram Bot Token

---

## 🔧 Installation

1. Clone this repo:

```
git clone https://github.com/yourusername/zabbix-telegram-status-bot.git
cd zabbix-telegram-status-bot
```

2. Install dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install python-telegram-bot requests
```

3. Edit the bot:

Open telegram_status_bot.py and set:

```
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ZABBIX_URL = "http://localhost/zabbix/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASS = "your_admin_password"
```

✅ Make sure the Zabbix password is quoted properly if it contains special characters like &.


▶️ Run the Bot

```
python3 telegram_status_bot.py
```

Then in your Telegram chat with the bot, run:

```
/status
```

🧠 Notes
- You must enable API access on your Zabbix frontend
- If you see Incorrect user name or password or account is temporarily blocked, wait a few minutes or reset the user’s failed attempts in the DB.

🛡️ Security Tips
- Never commit your bot token or password to public repos.
- Consider using .env files and python-dotenv for secure config.

---

## ⚙️ Running as a Systemd Service

To keep the bot running in the background and restart it on failures or system reboots:

1. Create a systemd service file

```
sudo nano /etc/systemd/system/zabbix-telegram-bot.service
```

Paste the following:
```
[Unit]
Description=Zabbix Telegram Status Bot
After=network.target

[Service]
Type=simple
User=stefan
WorkingDirectory=/opt/zabbix-telegram-bot
ExecStart=/opt/zabbix-telegram-bot/venv/bin/python3 /opt/zabbix-telegram-bot/telegram_status_bot.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
    🔁 Replace /opt/zabbix-telegram-bot and stefan with your actual path and username.

2. Reload systemd and start the service

```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable zabbix-telegram-bot.service
sudo systemctl start zabbix-telegram-bot.service
```

3. Check status or logs

Check service status
```
sudo systemctl status zabbix-telegram-bot
```

View live logs
```
journalctl -u zabbix-telegram-bot -f
```
