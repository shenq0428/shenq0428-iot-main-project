# 🅿️ Smart Parking Monitoring System (Grafana)

A real-time dashboard to monitor 3 floors and 10 parking slots, including battery levels and Telegram alert integration.

---

## 📂 Project Structure
```text
.
├── grafana/
│   ├── parking_dashboard.json   # The main dashboard template (JSON)
│   └── setup.sql                # SQL script to create the database table
├── assets/
│   ├── dashboard.png            # Main dashboard screenshot
│   └── parkinglot-alert.jpg     # Alert notification example
└── README.md                    # This guide
```


### 📥 How to Import the Dashboard

1. **Copy the JSON**: Go to the `grafana/` folder in this repo and copy the content of `parking_dashboard.json`.
2. **Grafana Import**: 
   - Open Grafana -> Click **Dashboards** -> **New** -> **Import**.
   - Paste the JSON code into the text area.
3. **Connect Your Database**: 
   - When prompted, select **your own MySQL data source** from the dropdown menu.
   - Click **Import**.

> **Note**: If you see "No Data", please ensure your MySQL table is named `parking_sensor_data` and has columns: `floor`, `space_id`, `status`, and `battery_level`.

### 🛠️ Prerequisites for "One-Click" Sync
To make this dashboard work immediately after importing the JSON, ensure your database has a table structured like this:

| Requirement | Value / Column Name |
| :--- | :--- |
| **Table Name** | `parking_data` (or update in query) |
| **Slot ID** | `slot_id` (e.g., F1-S01) |
| **Status** | `status` (0 = Green/Empty, 1 = Red/Occupied) |
| **Battery** | `battery_level` (0-100) |

### 🔔 How to setup Telegram Alerts (Mobile)

Since Alert Rules are not part of the Dashboard JSON, please follow these steps:

1. **Create Alert Rule**:
   - Edit the **"battery level"** panel.
   - Go to the **Alert** tab.
   - Set condition: `Triggered when any sensor's Battery Level < 30%.`.
2. **Contact Point**:
   - Go to **Alerting > Contact points**.
   - Create a new point called `Telegram_Alert`.
   - Choose **Telegram** and enter your **Bot API Token** and **Chat ID**.
3. **Link them**: Assign the `Telegram_Alert` to your alert rule.