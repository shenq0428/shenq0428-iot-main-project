import os
from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

app = Flask(__name__)

# --- 从环境变量中读取配置 ---
MYSQL_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

ALLOWED_IP = os.getenv("ALLOWED_SENDER_IP")
SAFE_TOKEN = os.getenv("DATA_SAFE_TOKEN")

@app.route('/upload_data', methods=['POST'])
def upload_data():
    # 打印请求来源 IP
    client_ip = request.remote_addr
    print(f"收到来自 IP: {client_ip} 的请求")

    # 1. 验证 IP (如果 ALLOWED_IP 为空则跳过验证，方便本地调试)
    if ALLOWED_IP and client_ip != ALLOWED_IP:
        print(f"🚫 拒绝访问：非法 IP {client_ip}")
        return jsonify({"status": "forbidden"}), 403
    
    # 2. 验证 Token
    auth_token = request.headers.get("X-Data-Token")
    if auth_token != SAFE_TOKEN:
        print("❌ Token 验证失败")
        return jsonify({"error": "wrong data token"}), 401
    
    # 3. 接收数据
    data = request.json 
    if not data:
        return jsonify({"status": "error", "message": "没收到任何数据"}), 400

    print(f"📦 收到来自电脑 A 的数据，共 {len(data)} 条。准备入库...")

    conn = None
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        insert_sql = """
            INSERT IGNORE INTO mysql_sensor_backup 
            (device_id, dts, pstr_bar_stp1, pstr_bar_stp2, pstr_psi_stp3, 
             pstr_psi_stp4, pdig_ma_dig1, pdig_ma_dig2, pdig_ma_dig3, qdb_timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        clean_data = [tuple(row) for row in data]
        cursor.executemany(insert_sql, clean_data)
        conn.commit()

        inserted_count = cursor.rowcount
        print(f"✅ 成功处理！实际新插入: {inserted_count} 条。")

        return jsonify({
            "status": "success", 
            "new_rows": inserted_count
        }), 200

    except Exception as e:
        print(f"❌ 入库出错: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 8888))
    debug = os.getenv("DEBUG_MODE", "False") == "True"
    
    print(f"🚀 电脑 B 接收端 API 尝试在端口 {port} 启动...")
    app.run(host='0.0.0.0', port=port, debug=debug)