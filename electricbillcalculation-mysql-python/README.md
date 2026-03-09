⚡ Electric Bill Calculation (MySQL + Python)
A automated utility billing system that calculates energy consumption differences and costs based on time-of-use (Morning/Night) rates.

.
├── mysqldatabase-create/    # SQL schema initialization files
│   ├── electricity_price_range.sql
│   ├── electricity_total_cost.sql
│   ├── electricity_usage_difference.sql
│   └── power_reading.sql
├── .env                     # Private configuration (Host, User, Pass)
├── .env.example             # Template for configuration
├── init_db.py               # 🛠️ One-click Database setup script
├── main.py                  # 🚀 Multi-threaded System Controller
├── power_reading.py         # Raw data collection (1 min)
├── electricity_usage_difference.py # Usage analyzer (5 min)
├── electricity_total_cost.py # Daily billing aggregator
├── README.md                # Project documentation
└── requirements.txt         # Python dependency list

## 📋 How It Works
1.Background Pipeline: The controller launches background threads to collect raw meter readings (every 60s) and analyze usage differences (every 5m).

2.Upsert Logic: Uses REPLACE INTO and DELETE/INSERT patterns. If the script re-runs, it overwrites old/incomplete data with the latest accuracy, ensuring Zero Redundancy.

3.Time-of-Use Classification: Automatically maps consumption to Morning (0.50) or Night (0.30) rates based on pre-defined pricing rules.

4.Billing Intelligence: Implements "Logic Date" shifting—electricity used between 00:00 and 08:00 is automatically credited to the previous day's bill to match actual usage cycles.
🛠️ Step 1: Database Initialization (REQUIRED)
Before running the Python script, you must set up the MySQL tables. While the script can create tables, manually importing these ensures your schema matches the intended logic perfectly.

🚀 Quick Start Guide
1. Clone & Install
git clone https://github.com/your-username/electricbillcalculation-mysql-python.git
cd electricbillcalculation-mysql-python
pip install -r requirements.txt

2. Copy .env.example into a new file name .env and insert your own configuration.
3.Auto-Setup: Run the initialization script to create all tables and default rates automatically(with this script you doesn't need to copy and run all sql query one by one):
python init_db.py

3.🎮 Running the System
You only need one terminal to run the entire system. Launch the multi-threaded controller:
python main.py

