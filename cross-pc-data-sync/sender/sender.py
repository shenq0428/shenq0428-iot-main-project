import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从 .env 读取配置
QUESTDB_URL = os.getenv("QUESTDB_URL")
QDB_USER = os.getenv("QDB_USER")
QDB_PASS = os.getenv("QDB_PASS")
B_API_URL = os.getenv("RECEIVER_API_URL")
SAFE_TOKEN = os.getenv("DATA_SAFE_TOKEN")

SYNC_FILE = "last_sync.txt"

def get_last_timestamp():
    if not os.path.exists(SYNC_FILE):
        return "2000-01-01T00:00:00.000000Z"
    try:
        with open(SYNC_FILE, "r") as f:
            ts = f.read().strip()
            return ts if ts else "2000-01-01T00:00:00.000000Z"
    except Exception:
        return "2000-01-01T00:00:00.000000Z"

def save_last_timestamp(ts):
    with open(SYNC_FILE, "w") as f:
        f.write(str(ts))

def send_to_api():
    last_ts = get_last_timestamp()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[检查时间: {current_time}]")
    print(f"🔍 正在检索比 {last_ts} 更新的数据...")

    # 1. 增量查询
    query = f"SELECT * FROM saymy_sensor_data WHERE dts > '{last_ts}' ORDER BY dts ASC"
    
    try:
        qdb_response = requests.get(
            QUESTDB_URL, 
            params={'query': query},
            auth=(QDB_USER, QDB_PASS),
            timeout=10
        )
        qdb_response.raise_for_status()
        data_json = qdb_response.json()
        dataset = data_json.get('dataset', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ 提取 QuestDB 数据失败: {e}")
        return
    
    if not dataset:
        print("No data to send.")
        return

    # 数据清洗
    clean_data = [
        [str(row[0]), str(row[1]), float(row[2]), float(row[3]),
         float(row[4]), float(row[5]), float(row[6]), float(row[7]),
         float(row[8]), str(row[9])] for row in dataset
    ]
            
    # 2. 推送数据
    print(f"📡 准备发送 {len(clean_data)} 行数据到电脑 B...")
    headers = {"X-Data-Token": SAFE_TOKEN, "Content-Type": "application/json"}
    
    try:
        api_response = requests.post(
            B_API_URL, 
            json=clean_data, 
            headers=headers, 
            timeout=15,
            proxies={"http": None, "https": None} 
        )
        
        if api_response.status_code == 200:
            print(f"✅ 成功! 电脑 B 回复: {api_response.json()}")
            save_last_timestamp(dataset[-1][1])
        else:
            print(f"❌ 失败，状态码: {api_response.status_code}, 内容: {api_response.text}")

    except Exception as e:
        print(f"❌ 连接异常: {e}")

if __name__ == "__main__":
    print(f"🚀 Sender 已启动，检查频率：1分钟/次")
    while True:
        send_to_api()
        time.sleep(60)