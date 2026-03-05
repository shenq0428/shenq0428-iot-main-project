import paho.mqtt.client as mqtt
import requests
import json
import os
from dotenv import load_dotenv

# 1. 加载 .env 文件（这样你就不必在代码里写死密码了）
load_dotenv()

# QuestDB 配置 (从环境变量读取)
QDB_URL = os.getenv("QDB_URL", "http://localhost:9000/exec")
# 注意：这里 QDB_AUTH 获取用户名和密码
QDB_AUTH = (os.getenv("QDB_USER", "admin"), os.getenv("QDB_PASS", "123456"))

# MQTT 配置 (从环境变量读取)
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")

# --- 2. MQTT 回调函数 ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ 已成功连接到 NovaPlus Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ 连接失败，返回码: {rc}")

def on_message(client, userdata, msg):
    print(f"--- 收到原始消息! Topic: {msg.topic} ---")
    print(f"DEBUG: Received raw message: {msg.payload}")
    
    try:
        # 解析原始 JSON 数据
        raw_payload = msg.payload.decode()
        data = json.loads(raw_payload)
        print(f"📩 收到数据，解析中...")

        # 提取数据（对应你刚才发给我的 JSON 结构）
        device_id = data.get("id")
        dts = data.get("dts")
        
        # 提取嵌套数值，如果缺失则默认为 0
        bar = data.get("PSTR_bar", {})
        psi = data.get("PSTR_psi", {})
        ma = data.get("PDIG_ma", {})

        # 构造 SQL 语句
        # 注意：这里我们直接把解析和写入放在一起，更简洁
        query = f"""
        INSERT INTO saymy_sensor_data (
            device_id, dts, 
            pstr_bar_stp1, pstr_bar_stp2, 
            pstr_psi_stp3, pstr_psi_stp4, 
            pdig_ma_dig1, pdig_ma_dig2, pdig_ma_dig3, 
            timestamp
        ) VALUES (
            '{device_id}', '{dts}', 
            {bar.get('stp1', 0)}, {bar.get('stp2', 0)}, 
            {psi.get('stp3', 0)}, {psi.get('stp4', 0)}, 
            {ma.get('dig1', 0)}, {ma.get('dig2', 0)}, {ma.get('dig3', 0)}, 
            now()
        );
        """

        # 发送到 QuestDB
        r = requests.get(QDB_URL, params={'query': query}, auth=QDB_AUTH)
        
        if r.status_code == 200:
            print(f"🚀 数据入库成功! (设备: {device_id})")
        else:
            print(f"❌ QuestDB 报错: {r.text}")

    except Exception as e:
        print(f"⚠️ 处理出错: {e}")


# --- 3. 启动客户端 ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASS)

print("正在尝试连接 NovaPlus Broker...")
try:
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    # 开始循环监听
    client.loop_forever()
except Exception as e:
    print(f"无法启动 MQTT 客户端: {e}")

