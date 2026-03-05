import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# 加载环境变量
load_dotenv()

# --- 从环境变量获取配置 ---
MQTT_HOST = os.getenv("MQTT_HOST", "hub.novaplus.my")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "data/#")

INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

# 初始化 InfluxDB 客户端
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

id_counter = 0

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ 已成功连接到 Broker! 正在订阅: {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ 连接失败，错误码: {rc}")

def on_message(client, userdata, msg):
    global id_counter
    try:
        payload = json.loads(msg.payload.decode())
        device_id = payload.get("id", "Unknown")
        print(f"📩 收到数据 (Topic: {msg.topic}): {device_id}")
        
        id_counter += 1

        # 安全地提取嵌套数据，避免缺失键导致崩溃
        pstr_bar = payload.get("PSTR_bar", {})
        pstr_psi = payload.get("PSTR_psi", {})
        pdig_ma = payload.get("PDIG_ma", {})

        # 构建 InfluxDB 数据点
        point = Point("pressure_data") \
            .tag("device_id", device_id) \
            .field("bar_stp1", float(pstr_bar.get("stp1", 0.0))) \
            .field("bar_stp2", float(pstr_bar.get("stp2", 0.0))) \
            .field("psi_stp3", float(pstr_psi.get("stp3", 0.0))) \
            .field("ma_dig1", float(pdig_ma.get("dig1", 0.0)))

        # 写入数据库
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(f"🚀 数据入库成功! (累计: {id_counter})")

    except Exception as e:
        print(f"⚠️ 数据处理跳过: {e} | 原始消息: {msg.payload[:50]}...")

# --- 启动 MQTT 客户端 ---
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print(f"正在连接到 {MQTT_HOST}...")
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_forever()
