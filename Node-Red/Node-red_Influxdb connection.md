canva: https://www.canva.com/design/DAHDpsl7nVc/BQWFxcslotzj6k54VOw_ew/edit?ui=e30

### 3. (JSON Source)
```json
[
    {
        "id": "7ea583e4b5528f0b",
        "type": "tab",
        "label": "Flow 1",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "df0e385ea7623379",
        "type": "tab",
        "label": "Flow 2",
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
        "id": "82e0af4e074e26fb",
        "type": "influxdb",
        "hostname": "127.0.0.1",
        "port": 8086,
        "protocol": "http",
        "database": "database",
        "name": "",
        "usetls": false,
        "tls": "",
        "influxdbVersion": "2.0",
        "url": "http://localhost:8086",
        "timeout": 10,
        "rejectUnauthorized": true
    },
    {
        "id": "7a96e1c97d356823",
        "type": "inject",
        "z": "7ea583e4b5528f0b",
        "name": "",
        "props": [
            {
                "p": "payload"
            },
            {
                "p": "topic",
                "vt": "str"
            }
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
        "wires": [
            [
                "13a4853fc89045e2"
            ]
        ]
    },
    {
        "id": "b4224507311b2178",
        "type": "mysql",
        "z": "7ea583e4b5528f0b",
        "mydb": "d997df3a7520156e",
        "name": "mysql-test_data1",
        "x": 650,
        "y": 40,
        "wires": [
            [
                "2b787f95c1438fad"
            ]
        ]
    },
    {
        "id": "13a4853fc89045e2",
        "type": "function",
        "z": "7ea583e4b5528f0b",
        "name": "Insert fake data ",
        "func": "let device = \"MJM_Sensor_Alpha\";\nlet voltage = 238.5;\n\nmsg.topic = `INSERT INTO test_data (device_name, voltage_value) VALUES ('${device}', ${voltage})`;\nreturn msg;",
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 400,
        "y": 40,
        "wires": [
            [
                "b4224507311b2178"
            ]
        ]
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
        "id": "761f077ad7fc345b",
        "type": "debug",
        "z": "7ea583e4b5528f0b",
        "name": "debug 2",
        "active": false,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "false",
        "statusVal": "",
        "statusType": "auto",
        "x": 830,
        "y": 220,
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
        "wires": [
            [
                "761f077ad7fc345b"
            ]
        ]
    },
    {
        "id": "19e1dd77cfbac9c9",
        "type": "function",
        "z": "7ea583e4b5528f0b",
        "name": "Insert random data ",
        "func": "// 1. Generate a random voltage between 230V and 245V\n// Formula: (Random 0-1 * Range) + Minimum\nlet randomVoltage = (Math.random() * 15) + 230;\n\n// 2. Round it to 2 decimal places so it looks clean\nrandomVoltage = parseFloat(randomVoltage.toFixed(2));\n\nlet device = \"MJM_Sensor_Alpha\";\n\n// 3. Build the SQL Query with the dynamic variable\nmsg.topic = `INSERT INTO test_data (device_name, voltage_value) VALUES ('${device}', ${randomVoltage})`;\n\nreturn msg;",
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 410,
        "y": 220,
        "wires": [
            [
                "4547060b08ede54a"
            ]
        ]
    },
    {
        "id": "72dad0eadb67c3a6",
        "type": "inject",
        "z": "7ea583e4b5528f0b",
        "d": true,
        "name": "5s",
        "props": [
            {
                "p": "payload"
            },
            {
                "p": "topic",
                "vt": "str"
            }
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
        "wires": [
            [
                "19e1dd77cfbac9c9"
            ]
        ]
    },
    {
        "id": "7319ba68af2d9cbd",
        "type": "influxdb out",
        "z": "df0e385ea7623379",
        "influxdb": "82e0af4e074e26fb",
        "name": "",
        "measurement": "",
        "precision": "",
        "retentionPolicy": "",
        "database": "database",
        "precisionV18FluxV20": "ms",
        "retentionPolicyV18Flux": "",
        "org": "first-Org",
        "bucket": "node_red_sensor_data",
        "x": 550,
        "y": 140,
        "wires": []
    },
    {
        "id": "807651d7a68da122",
        "type": "function",
        "z": "df0e385ea7623379",
        "name": "function 1",
        "func": "// 1. Generate a random voltage between 230V and 245V\nlet voltage = (Math.random() * 15) + 230;\nvoltage = parseFloat(voltage.toFixed(2));\n\n// 2. Construct the InfluxDB 2.0 message format\n// The InfluxDB node automatically treats the payload as the \"field\" value\nmsg.payload = voltage;\n\n// 3. Set the Measurement (Equivalent to a Table name in SQL)\nmsg.measurement = \"industrial_voltage\";\n\n// 4. Add Tags (Metadata used for filtering and high-speed indexing)\nmsg.tags = {\n    device_id: \"MJM_Sensor_01\",\n    factory_floor: \"Section_A\"\n};\n\nreturn msg;",
        "outputs": 1,
        "timeout": 0,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 300,
        "y": 140,
        "wires": [
            [
                "7319ba68af2d9cbd"
            ]
        ]
    },
    {
        "id": "0f9d53ba767b6328",
        "type": "inject",
        "z": "df0e385ea7623379",
        "d": true,
        "name": "",
        "props": [
            {
                "p": "payload"
            },
            {
                "p": "topic",
                "vt": "str"
            }
        ],
        "repeat": "5",
        "crontab": "",
        "once": false,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 130,
        "y": 140,
        "wires": [
            [
                "807651d7a68da122"
            ]
        ]
    },
    {
        "id": "eb71410f526f54da",
        "type": "global-config",
        "env": [],
        "modules": {
            "node-red-node-mysql": "3.0.0",
            "node-red-contrib-influxdb": "0.7.0"
        }
    }
]
