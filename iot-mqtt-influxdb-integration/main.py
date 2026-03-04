import os
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

# 加载配置
load_dotenv()

# --- 1. 配置加载 ---
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# InfluxDB 配置
client_influx = InfluxDBClient(
    url=os.getenv("INFLUX_URL"),
    token=os.getenv("INFLUX_TOKEN"),
    org=os.getenv("INFLUX_ORG")
)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)
bucket = os.getenv("INFLUX_BUCKET")

# --- 2. MQTT 回调 ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to Broker: {MQTT_HOST}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ Connection failed, code: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        device_id = data.get("id")
        
        # 提取数值
        bar = data.get("PSTR_bar", {})
        psi = data.get("PSTR_psi", {})
        ma = data.get("PDIG_ma", {})

        # 构造 InfluxDB Point (Line Protocol)
        point = Point("sensor_data") \
            .tag("device_id", device_id) \
            .field("bar_stp1", float(bar.get('stp1', 0))) \
            .field("bar_stp2", float(bar.get('stp2', 0))) \
            .field("psi_stp3", float(psi.get('stp3', 0))) \
            .field("psi_stp4", float(psi.get('stp4', 0))) \
            .field("ma_dig1", float(ma.get('dig1', 0))) \
            .field("ma_dig2", float(ma.get('dig2', 0))) \
            .field("ma_dig3", float(ma.get('dig3', 0)))

        # 写入数据库
        write_api.write(bucket=bucket, record=point)
        print(f"🚀 Data ingested to InfluxDB! (Device: {device_id})")

    except Exception as e:
        print(f"⚠️ Error processing message: {e}")

# --- 3. 运行 ---
client = mqtt.Client()
client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"❌ Client error: {e}")
