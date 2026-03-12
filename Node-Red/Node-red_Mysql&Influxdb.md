# Multi-Tier IoT Data Pipeline: MySQL & InfluxDB Integration

This project demonstrates an advanced industrial data pipeline that ingests MQTT-style telemetry and implements **Polyglot Persistence**. It intelligently routes data into two separate databases based on the data's nature: **MySQL** for structured metadata (a.1) and **InfluxDB** for high-frequency metrics (a.2).

## 🚀 Node-RED Data Pipeline

The pipeline is designed to simulate industrial sensor behavior and handle data decoupling at the edge.

### 1. Flow Description
- **Inject Node**: Acts as the system heartbeat, triggering data generation every 3 seconds.
- **Function Node**: The "Brain" of the flow. It parses incoming JSON data and splits it:
    - **a.1 (Relational)**: Prepares `device_name` and `status` for SQL logging.
    - **a.2 (Time-Series)**: Prepares raw `voltage` and `tags` for InfluxDB streaming.
- **MySQL Node**: Executes persistent relational storage for audit trails and status monitoring.
- **InfluxDB Node**: Handles high-velocity telemetry data with optimized time-series storage.
- **Catch Node**: A centralized error handler that captures any background connection issues without disrupting the flow.



---

## 🗄️ Database Setup

Note: You must initialize both databases before deploying the Node-RED flow.

### A. MySQL Configuration
Execute this script to create the logging schema:
```sql
-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS smart_mill_db;
USE smart_mill_db;

-- 2. Create the Table for Metadata (a.1)
CREATE TABLE IF NOT EXISTS device_status_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(50),
    status_code INT,
    log_message VARCHAR(100) DEFAULT 'DATA_RECEIVED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
