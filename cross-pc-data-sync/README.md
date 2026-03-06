# 🛰️ Cross-PC Data Sync (QuestDB to MySQL)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional, secure, and incremental data synchronization system for IoT environments.

---

## 🛠️ Quick Start Guide

| Step | Action | Command / Details |
| :--- | :--- | :--- |
| **1. Install** | Install dependencies on **both** PCs | `pip install -r requirements.txt` |
| **2. Config** | Setup `.env` from `.env.example` | Create `.env` in `receiver/` and `sender/` folders |
| **3. IP Lookup** | Find your IPv4 via CMD | Run `ipconfig` in Command Prompt |
| **4. PC A Setup** | Configure **Sender** | Set `RECEIVER_API_URL` to PC B's IP address |
| **5. PC B Setup** | Configure **Receiver** | Set `ALLOWED_SENDER_IP` to PC A's IP address |
| **6. Run B** | Start the API on **PC B** | `python receiver/receiver.py` |
| **7. Run A** | Start syncing on **PC A** | `python sender/sender.py` |

---

## 🔍 Network & Troubleshooting Reference

| Category | Item | Solution / Command |
| :--- | :--- | :--- |
| **Connection** | **Tailscale** (Recommended) | Use `100.x.x.x` IP for static, cross-network syncing. |
| **Security** | **Auth Token** | Ensure `DATA_SAFE_TOKEN` is identical in both `.env` files. |
| **Firewall** | **Open Port 8888** | `New-NetFirewallRule -DisplayName "Flask" -LocalPort 8888 -Protocol TCP -Action Allow` |
| **Syncing** | **Incremental Log** | `last_sync.txt` is auto-generated to prevent data duplication. |

---

## 📂 Project Structure

```text
cross-pc-data-sync/
├── receiver/
│   ├── .env                    # (Private) MySQL credentials & Auth Token
│   ├── .env.example            # Environment template for PC B
│   ├── .gitignore              # Protects .env from leaks
│   ├── receiver.py             # Main Flask API
│   └── Receiver_QuestDB_Mysql.py # Advanced receiver logic
├── sender/
│   ├── .env                    # (Private) Source credentials & Target IP
│   ├── .env.example            # Environment template for PC A
│   ├── .gitignore              # Protects .env from leaks
│   ├── sender.py               # Main data fetcher and pusher
│   ├── Sender_QuestDB_Mysql.py # Advanced sender logic
│   └── last_sync.txt           # (Auto-generated) Stores sync progress
├── requirements.txt            # Python dependencies
└── README.md                   # This instruction file