
# 🚀 IoT Data Bridge: MySQL to PostgreSQL Sync Service

This project is a high-performance data synchronization service built with **FastAPI**. It functions as a real-time monitor that observes a MySQL database (typically managed via phpMyAdmin) and automatically replicates new entries into a **PostgreSQL** database for advanced analytics or backup.

## 📂 Folder Structure

```text
.
├── .env                 # Private configuration file (Created by you)
├── .env.example         # Template for configuration
├── .gitignore           # Files to be ignored by Git
├── main.py              # Main service script (FastAPI + Sync Logic)
├── monitoring.py        # backup script of main.py
├── README.md            # Project documentation
└── requirements.txt     # Python dependency list
```
---

## 📋 How It Works

1.  **Background Monitor**: Upon startup, the script launches a dedicated background thread that polls the MySQL source every second.
2.  **Incremental Sync**: It tracks the `last_synced_id` to ensure only new records are fetched, preventing redundant data processing.
3.  **Cross-Database Mapping**: It extracts `val`, `increment`, and `timestamp` from MySQL and maps them directly to the PostgreSQL schema.
4.  **Data Integrity**: Utilizes PostgreSQL's `UNIQUE` constraint on the timestamp to prevent duplicate entries during sync recovery.

---
graph LR
    A[MySQL / phpMyAdmin] -- "Polling New IDs" --> B{Python Worker}
    B -- "Transform Data" --> C[(PostgreSQL)]
    B -- "Status API" --> D[Browser/User]
    

## 🛠️ Database Setup (Required)

Before running the script, you must create the target table in your **PostgreSQL** database. Run the following SQL command in your PostgreSQL query tool (e.g., pgAdmin or DBeaver):

```sql
CREATE TABLE IF NOT EXISTS public.table_3_apitesting
(
    id SERIAL, 
    "timestamp" timestamp without time zone,
    val bigint,
    increment bigint,
    CONSTRAINT table_3_apitesting_pkey1 PRIMARY KEY (id),
    CONSTRAINT unique_timestamp UNIQUE ("timestamp")
);
```

----
- **step 1 (Clone)**:git clone [https://github.com/shenq0428/shenq0428-iot-main-project.git](https://github.com/shenq0428/shenq0428-iot-main-project.git)
cd mysql-to-postgres-sync
- **step 2 (Install Dependencies)**:pip install -r requirements.txt
- **step 3 (Setup Config)**: copy the example from (.env.example) folder ,create a newfolder name (.env) and setup own configuration.
- **step 4 (Run)**: Run the service using Uvicorn -> uvicorn monitoring:app --reload
----

---

## ✅ How to Verify & Troubleshoot

Open your browser and visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 1. Check `status`
* **If it shows `"status": "Running"`**: The "Background Sentry" (监控小兵) is alive and patrolling your MySQL database.
* **If it shows `"Error: ..."`**: There is a connection issue. Check your database credentials in your `.env` file.

### 2. Check `env_check`
* **Success**: Ensure `mysql_db` and `pg_db` display your correct database names.
* **Failure**: If these fields show **`null`**, the script failed to read your `.env` file. Check if the file is named correctly (ensure there is no `.txt` extension) and is located in the root folder.

### 3. Verification
* **Insert Data**: Add a new row in **phpMyAdmin (MySQL)**. 
* **Observe**: Refresh the API page (`http://127.0.0.1:8000`); the `sync_count` should increase, and the data should appear in **PostgreSQL** automatically.

---