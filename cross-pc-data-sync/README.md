```
cross-pc-data-sync/
├── receiver/
│   ├── .env                    # (Local & Private) Stores database credentials and Auth Token
│   ├── .env.example            # Environment template for public reference
│   ├── .gitignore              # Ensures .env is never uploaded to GitHub
│   ├── receiver.py             # Main Flask API for receiving data
│   └── Receiver_QuestDB_Mysql.py # Backup or advanced receiver logic
├── sender/
│   ├── .env                    # (Local & Private) Stores source credentials and Receiver IP
│   ├── .env.example            # Environment template for public reference
│   ├── .gitignore              # Ensures .env is never uploaded to GitHub
│   ├── sender.py               # Main script for fetching and pushing data
│   ├── Sender_QuestDB_Mysql.py # Backup or advanced sender logic
│   └── last_sync.txt           # (Auto-generated) Stores the incremental sync progress
├── requirements.txt            # Python dependencies for both scripts
└── README.md                   # Installation, configuration, and network debugging guide
```

🛠️ Quick Start
1. Installation
Run the following command on both computers:

Bash
pip install -r requirements.txt
2. Configuration (.env Setup)
You need to create a .env file in each folder. Use .env.example as a template.

On Computer B (Receiver): Fill in your MySQL credentials and set a DATA_SAFE_TOKEN.

On Computer A (Sender): Fill in your QuestDB credentials and set the RECEIVER_API_URL using PC B's IP.

3. Finding Your IP Address
To link the two computers, you need their IP addresses:

Press Win + R, type cmd, and hit Enter.

Type ipconfig and find the IPv4 Address.

PC A's IP: Add this to PC B's .env under ALLOWED_SENDER_IP.

PC B's IP: Add this to PC A's .env under RECEIVER_API_URL (e.g., http://10.x.x.x:8888/upload_data).

🚀 Troubleshooting & Tips
🔗 Use Tailscale (Recommended)
If the computers are in different locations (not on the same Wi-Fi), use Tailscale.

Look for the 100.x.x.x address in ipconfig after installing Tailscale.

Tailscale IPs are static and secure, making them perfect for this setup.

🧱 Windows Firewall
If PC A gets a "Connection Refused" error, you must open port 8888 on PC B.
Run this in PowerShell as Administrator:

PowerShell
New-NetFirewallRule -DisplayName "Flask_Receiver" -Direction Inbound -LocalPort 8888 -Protocol TCP -Action Allow
📦 Incremental Sync
The last_sync.txt file is automatically generated in the sender/ folder after the first successful sync.

It remembers the last timestamp sent.

If you delete this file, the script will re-sync all historical data from the beginning.

🛡️ Security
IP Whitelisting: Only the designated Sender IP can talk to the Receiver.

Token Authorization: Every request must include the X-Data-Token header.

Environment Safety: Your real passwords and tokens are stored in .env, which is ignored by Git to prevent leaks.




---

### ✅ 最后的发布清单 (Ready to Push?)
1.  **检查依赖**：确认 `requirements.txt` 里有 `python-dotenv`。
2.  **检查安全**：确认你没把真实的 `.env` 传上去（`git status` 不应该看到它们）。
3.  **运行测试**：在本地运行 `receiver.py` 看看能不能正常启动。

**这就是你的完整 README 了！如果你觉得已经准备好了，我会非常乐意帮你生成最后的 Git Push 命令。**