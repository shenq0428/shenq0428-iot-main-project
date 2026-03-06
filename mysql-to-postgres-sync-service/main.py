import os
import time
import threading
import mysql.connector
import psycopg2
from fastapi import FastAPI
from dotenv import load_dotenv

# 加载配置
load_dotenv()

app = FastAPI()

# 状态记录器
monitor_stats = {
    "last_synced_id": 0,
    "status": "Initializing",
    "sync_count": 0
}

def start_monitoring():
    monitor_stats["status"] = "Running"
    interval = int(os.getenv("SYNC_INTERVAL", 1))
    
    while True:
        try:
            # 连接 MySQL
            m_conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASS"),
                database=os.getenv("MYSQL_DB")
            )
            m_cur = m_conn.cursor(dictionary=True)
            
            # 查询新数据
            query = "SELECT id, val, increment, timestamp FROM table_3 WHERE id > %s ORDER BY id ASC"
            m_cur.execute(query, (monitor_stats["last_synced_id"],))
            new_rows = m_cur.fetchall()
            
            if new_rows:
                # 连接 PostgreSQL
                p_conn = psycopg2.connect(
                    host=os.getenv("PG_HOST"),
                    user=os.getenv("PG_USER"),
                    password=os.getenv("PG_PASS"),
                    database=os.getenv("PG_DB")
                )
                p_cur = p_conn.cursor()
                
                for row in new_rows:
                    insert_query = """
                        INSERT INTO table_3_apitesting (timestamp, val, increment) 
                        VALUES (%s, %s, %s)
                        ON CONFLICT (timestamp) DO NOTHING
                    """
                    p_cur.execute(insert_query, (row['timestamp'], row['val'], row['increment']))
                    monitor_stats["last_synced_id"] = row['id']
                    monitor_stats["sync_count"] += 1
                
                p_conn.commit()
                p_cur.close()
                p_conn.close()
            
            m_cur.close()
            m_conn.close()
            
        except Exception as e:
            print(f"❌ 同步报错: {e}")
            monitor_stats["status"] = f"Error: {str(e)}"
        
        time.sleep(interval)

# 启动后台监控线程
threading.Thread(target=start_monitoring, daemon=True).start()

@app.get("/")
def check_status():
    return {
        "title": "MySQL -> PostgreSQL Real-time Sync",
        "stats": monitor_stats,
        "env_check": {
            "mysql_db": os.getenv("MYSQL_DB"),
            "pg_db": os.getenv("PG_DB")
        }
    }