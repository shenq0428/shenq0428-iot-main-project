Canva: https://www.canva.com/design/DAHDnxF14RQ/xtA7TAxMSf_mBrIF1Ui8gA/edit?utm_content=DAHDnxF14RQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Reference video: https://www.youtube.com/watch?v=w1SRebmR_NY


## 🚀 Node-RED Data Pipeline

This project features an automated data pipeline designed to simulate industrial sensor data and persist it into a MySQL database. It demonstrates the integration between IoT edge logic (Node-RED) and relational database management (MySQL).

### 1. (Flow Description)
- Inject Node: Acts as the trigger (manual or interval-based).
- Function Node: Simulates sensor logic by generating device metadata and constructing the SQL INSERT statement.
- MySQL Node: Establishes the connection to the local database and executes the query.
- Debug Node: Provides real-time feedback on the database response.

Note before you import remember to create the database in Mysql
```
-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS node_red_db;

-- 2. Switch to the database
USE node_red_db;

-- 3. Create the Table
CREATE TABLE IF NOT EXISTS test_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(50),
    voltage_value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
### 2. (How to Import)
1. Open your Node-RED Editor.
2. Click the Menu (three bars) in the top-right corner.
3. Select Import.
4. Paste the JSON code below into the input box and click Import.
Note: Double-click the MySQL node to update your database credentials (username and password) before clicking Deploy.

### 3. (JSON Source)
```json
[
    {
        "id": "7ea583e4b5528f0b",
        "type": "tab",
        "label": "Industrial Flow",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "d997df3a7520156e",
        "type": "MySQLdatabase",
        "name": "",
        "host": "127.0.0.1",
        "port": "3306",
        "db": "node_red_db",
        "tz": "",
        "charset": "UTF8"
    },
    {
        "id": "7a96e1c97d356823",
        "type": "inject",
        "z": "7ea583e4b5528f0b",
        "name": "Manual Test",
        "props": [
            { "p": "payload" },
            { "p": "topic", "vt": "str" }
        ],
        "repeat": "",
        "crontab": "",
        "once": false,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 220,
        "y": 40,
        "wires": [ ["13a4853fc89045e2"] ]
    },
    {
        "id": "b4224507311b2178",
        "type": "mysql",
        "z": "7ea583e4b5528f0b",
        "mydb": "d997df3a7520156e",
        "name": "mysql-test_data1",
        "x": 650,
        "y": 40,
        "wires": [ ["2b787f95c1438fad"] ]
    },
    {
        "id": "13a4853fc89045e2",
        "type": "function",
        "z": "7ea583e4b5528f0b",
        "name": "Static Data",
        "func": "let device = \"MJM_Sensor_Alpha\";\nlet voltage = 238.5;\n\nmsg.topic = `INSERT INTO test_data (device_name, voltage_value) VALUES ('${device}', ${voltage})`;\nreturn msg;",
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 400,
        "y": 40,
        "wires": [ ["b4224507311b2178"] ]
    },
    {
        "id": "2b787f95c1438fad",
        "type": "debug",
        "z": "7ea583e4b5528f0b",
        "name": "debug 1",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "false",
        "statusVal": "",
        "statusType": "auto",
        "x": 830,
        "y": 40,
        "wires": []
    },
    {
        "id": "4547060b08ede54a",
        "type": "mysql",
        "z": "7ea583e4b5528f0b",
        "mydb": "d997df3a7520156e",
        "name": "mysql-test_data2",
        "x": 650,
        "y": 220,
        "wires": [ ["761f077ad7fc345b"] ]
    },
    {
        "id": "19e1dd77cfbac9c9",
        "type": "function",
        "z": "7ea583e4b5528f0b",
        "name": "Random Data Generator",
        "func": "let randomVoltage = (Math.random() * 15) + 230;\nrandomVoltage = parseFloat(randomVoltage.toFixed(2));\nlet device = \"MJM_Sensor_Alpha\";\nmsg.topic = `INSERT INTO test_data (device_name, voltage_value) VALUES ('${device}', ${randomVoltage})`;\nreturn msg;",
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 410,
        "y": 220,
        "wires": [ ["4547060b08ede54a"] ]
    },
    {
        "id": "72dad0eadb67c3a6",
        "type": "inject",
        "z": "7ea583e4b5528f0b",
        "d": true,
        "name": "Auto Trigger 5s",
        "props": [
            { "p": "payload" },
            { "p": "topic", "vt": "str" }
        ],
        "repeat": "5",
        "crontab": "",
        "once": false,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 210,
        "y": 220,
        "wires": [ ["19e1dd77cfbac9c9"] ]
    }
]
