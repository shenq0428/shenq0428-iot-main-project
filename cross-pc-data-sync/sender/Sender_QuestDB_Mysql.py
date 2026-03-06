import requests
#import json
import time
import os
from datetime import datetime


# QuestDB configuration
QUESTDB_URL = ""
QDB_USER = ""
QDB_PASS = ""

# 电脑 B 的 IP 地址和 API 路径 (确保路径 /upload_data 拼写正确)
# 找到这一行并修改
B_API_URL = ""

SAFE_TOKEN = ""

SYNC_FILE="last_sync.txt"
#-----------------log.txt---------------
def get_last_timestamp():
    if not os.path.exists(SYNC_FILE):
            return "2000-01-01T00:00:00.000000Z"
    try:
        with open(SYNC_FILE,"r") as f:
            ts = f.read().strip()
            return ts if ts else "2000-01-01T00:00:00.000000Z"
    except Exception:
        return "2000-01-01T00:00:00.000000Z"
def save_last_timestamp(ts):
    with open (SYNC_FILE,"w") as f:
        f.write(str(ts))
#---------------------end log.txt--------------
    
def send_to_api():
    last_ts = get_last_timestamp()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[检查时间: {current_time}]")
    print(f"🔍 正在检索比 {last_ts} 更新的数据...")

    # 1. 增量查询 (注意: 这里的 dts也就是timestamp 必须是你 QuestDB 表里的时间戳字段名)
    query = f"SELECT * FROM saymy_sensor_data WHERE dts > '{last_ts}' ORDER BY timestamp ASC"
    
    try:
        qdb_response = requests.get(
            QUESTDB_URL, 
            params={'query': query},
            auth=(QDB_USER, QDB_PASS),
            timeout=10
        )
        #检查网络请求是否成功
        qdb_response.raise_for_status()
        #把数据库回传的“包裹”拆开，转成 Python 字典
        data_json = qdb_response.json()
        #从包裹里专门取出那部分“数据行”
        dataset = data_json.get('dataset', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ 提取 QuestDB 数据失败: {e}")
        return
    
    
    if not dataset:
        print("No data to send.")
        return

    # 数据清洗
    clean_data = []
    for row in dataset:
        processed_row = [
            str(row[0]), str(row[1]), float(row[2]), float(row[3]),
            float(row[4]), float(row[5]), float(row[6]), float(row[7]),
            float(row[8]), str(row[9])
        ]
        clean_data.append(processed_row)
            
    # 2. 通过 POST 把数据推给电脑 B 的 API
    print(f"📡 准备发送 {len(clean_data)} 行数据到电脑 B...")
    
    headers = {
        "X-Data-Token": SAFE_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        # 【核心调试块】
        api_response = requests.post(
            B_API_URL, 
            json=clean_data, # 建议发送清洗后的数据
            headers=headers, 
            timeout=15,
            proxies={"http": None, "https": None} # 强制跳过系统代理，防止干扰
        )
        
        if api_response.status_code == 200:
            print(f"✅ 成功! 电脑 B 回复: {api_response.json()}")
            last_timestamp_in_batch = dataset [-1][1]
            save_last_timestamp(last_timestamp_in_batch)
        elif api_response.status_code == 401:
            print(f"❌ 失败: Token (密码) 不正确")
        elif api_response.status_code == 403:
            print(f"❌ 失败: 电脑 B 的 ALLOWED_IP 屏蔽了你的 IP")
        elif api_response.status_code == 404:
            print(f"❌ 失败: 找不到接口路径，请检查 B_API_URL 是否漏写了 /upload_data")
        else:
            print(f"❌ 异常状态码: {api_response.status_code}")
            print(f"错误内容: {api_response.text}")

    except requests.exceptions.ProxyError:
        print("❌ 调试建议: 检测到代理冲突！请关闭 VPN 或公司代理软件后再试。")
    except requests.exceptions.ConnectTimeout:
        print("❌ 调试建议: 连接超时！信号传不到电脑 B。请检查电脑 B 的防火墙是否真的开了 8888 端口。")
    except requests.exceptions.ConnectionError:
        print("❌ 调试建议: 连接被拒绝！电脑 B 可能没运行 Flask，或者拒绝了该连接。")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")

if __name__ == "__main__":
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start from {start_time} .Check every 1 minute")
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_to_api()
        print(f"checked time {current_time}")
        time.sleep(60)