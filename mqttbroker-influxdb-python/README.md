# 🚀 IoT Data Bridge: MQTT to InfluxDB

This project demonstrates how to build a real-time IoT data pipeline using Python. It subscribes to sensor data from an **MQTT Broker**, parses nested JSON payloads, and stores them into **InfluxDB** for time-series visualization and monitoring.

---

## 📋 Project Overview

In Industrial IoT (IIoT), sensors often send high-frequency data in JSON format. This project handles:
1. **Protocol Conversion**: Bridging MQTT (Pub/Sub) to InfluxDB (Flux/Bucket).
2. **Data Parsing**: Extracting values from nested structures (e.g., `PSTR_bar`, `PDIG_ma`) with safety fallbacks.
3. **Storage**: Storing data as **Points** (Fields & Tags) for high-speed querying and dashboarding in InfluxDB or Grafana.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Protocol**: MQTT (Paho-MQTT v2)
- **Database**: **InfluxDB** (Time-series Database)
- **Security**: Dotenv (Managing credentials and tokens safely)

---

## 📊 Architecture

```mermaid
graph LR
    A[Sensors] -- "JSON Payload" --> B(MQTT Broker <br/><b>Data Source</b>)
    B -- "Subscribe" --> C{Python Script <br/><b>The Worker</b>}
    C -- "Write API" --> D[(InfluxDB <br/><b>Destination</b>)]
    
    %% Style definitions
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style D fill:#78c2ff,stroke:#333,stroke-width:2px
```
----
Quick Start
- **step 1 (Clone)**:git clone https://github.com/shenq0428/shenq0428-iot-main-project.git
        cd mqttbroker-questdb-python
- **step 2 (Install Dependencies)**:pip install -r requirements.txt
- **step 3 (Setup Config)**: copy the example from (.env.example) folder ,create a newfolder name (.env) and setup own configuration.
- **step 4 (Run)**: run the main code -> python main.py
----
