from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# --- 电脑 B 本地的 MySQL 配置 ---
MYSQL_CONFIG = {
    "host": "",       # 它是给电脑 B 自己看的，所以用 localhost
    "user": "",
    "password": "",         # 换成你 B 电脑的密码
    "database": ""      # 确保你已经创建了这个数据库
}

ALLOWED_IP = ""  # 假设这是电脑 A 的固定 IP
SAFE_TOKEN = ""

@app.route('/upload_data', methods=['POST'])
def upload_data():
    print(f"收到来自 IP: {request.remote_addr} 的请求") # 加这一行在 Console 打印出来

    if request.remote_addr != ALLOWED_IP:
        print(f"{request.remote_addr}")
        return jsonify({"status":"forbidden"}),403
    
    #-- second authorization --🙂
    auth_token = request.headers.get("X-Data-Token")
    if auth_token != SAFE_TOKEN:
        print("correct IP but is not the same DATA TOKEN")
        return jsonify({"error":"wrong data token"}),401
    
    # 1. 接收从电脑 A 发过来的 JSON 数据包
    data = request.json 
    
    if not data:
        return jsonify({"status": "error", "message": "没收到任何数据"}), 400

    print(f"📦 收到来自电脑 A 的数据，共 {len(data)} 条。准备入库...")

    conn = None
    try:
        # 2. 连接电脑 B 本地的 MySQL
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # 3. 准备 SQL 语句 (INSERT IGNORE 依然是你的护身符)
        insert_sql = """
            INSERT IGNORE INTO mysql_sensor_backup 
            (device_id, dts, pstr_bar_stp1, pstr_bar_stp2, pstr_psi_stp3, 
             pstr_psi_stp4, pdig_ma_dig1, pdig_ma_dig2, pdig_ma_dig3, qdb_timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 4. 数据转换：API 收到的数据是列表，executemany 需要元组列表
        clean_data = [tuple(row) for row in data]

        # 5. 执行批量插入
        cursor.executemany(insert_sql, clean_data)
        conn.commit()

        inserted_count = cursor.rowcount
        print(f"✅ 成功处理！实际新插入: {inserted_count} 条。")

        # 6. 给电脑 A 回个信，告诉它成功了
        return jsonify({
            "status": "success", 
            "message": "Data received and saved", 
            "new_rows": inserted_count
        }), 200

    except Exception as e:
        print(f"❌ 入库出错: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# --- 又是这个开关！ ---
if __name__ == "__main__":
    print("🚀 电脑 B 接收端 API 尝试启动...")
    try:
        # 开启 debug=True
        app.run(host='0.0.0.0', port=8888, debug=False)#change debug to True to test
    except Exception as e:
        print(f"❌ 启动失败，原因: {e}")