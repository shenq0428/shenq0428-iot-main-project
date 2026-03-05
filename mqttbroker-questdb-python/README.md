pythonscript_mqttbroker_questdb.py
# 🚀 IoT Data Bridge: MQTT to QuestDB

This project demonstrates how to build a real-time IoT data pipeline using Python. It subscribes to sensor data from an **MQTT Broker**, parses nested JSON payloads, and stores them into **QuestDB** for high-performance time-series analysis.

---

## 📋 Project Overview

In Industrial IoT (IIoT), sensors often send high-frequency data in JSON format. This project handles:
1. **Protocol Conversion**: Bridging MQTT (Pub/Sub) to QuestDB (SQL / ILP).
2. **Data Parsing**: Extracting values from nested structures (e.g., `PSTR_bar`, `PDIG_ma`).
3. **Storage**: Efficiently saving data for visualization in tools like Grafana using QuestDB's SQL capabilities.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Protocol**: MQTT (Paho-MQTT)
- **Database**: **QuestDB** (High-performance Time-series SQL Database)
- **Security**: Dotenv (Managing credentials safely)

---

## 📊 Architecture

```mermaid
graph LR
    A[Sensors] -- JSON Over MQTT --> B(MQTT Broker)
    B -- Subscribe --> C{Python Script}
    C -- Parse & Insert --> D[(QuestDB)]
    D -- SQL Query --> E[Grafana]
```

----
- **step 1 (Clone)**:git clone https://github.com/shenq0428/shenq0428-iot-main-project.git
        cd mqttbroker-questdb-python
- **step 2 (Install Dependencies)**:pip install -r requirements.txt
- **step 3 (Setup Config)**: setup own configuration in .env folder
- **step 4 (Run)**: run the main code -> python main.py
