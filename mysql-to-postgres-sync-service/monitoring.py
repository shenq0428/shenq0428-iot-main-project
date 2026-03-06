from fastapi import FastAPI
import mysql.connector
import psycopg2
from psycopg2.extras import RealDictCursor
import threading
import time

app = FastAPI()

# --- 配置区 ---
MYSQL_CONFIG = {
    "host": "",
    "user": "",
    "password": "",  
    "database": ""
}

PG_CONFIG = {
    "host": "",
    "user": "",
    "password": "",
    "database": ""
}

# 监控员的状态记录
monitor_stats = {
    "last_synced_id": 0,
    "status": "Initializing",
    "sync_count": 0
}

# --- 监控逻辑：这就是你的“后台监控系统” ---
def start_monitoring():
    monitor_stats["status"] = "Running"
    while True:
        try:
            m_conn = mysql.connector.connect(**MYSQL_CONFIG)
            m_cur = m_conn.cursor(dictionary=True)
            
            # 关键修改：我们要查出所有的列，包括 timestamp 和 increment
            m_cur.execute("SELECT id, val, increment, timestamp FROM table_3 WHERE id > %s ORDER BY id ASC", 
                         (monitor_stats["last_synced_id"],))
            new_rows = m_cur.fetchall()
            
            if new_rows:
                p_conn = psycopg2.connect(**PG_CONFIG)
                p_cur = p_conn.cursor()
                
                for row in new_rows:
                    # 关键修改：把从 MySQL 拿到的所有灵魂（数据）全部塞进 PostgreSQL
                    insert_query = """
                        INSERT INTO table_3_apitesting (timestamp,val, increment) 
                        VALUES (%s, %s, %s)
                        ON CONFLICT (timestamp) DO NOTHING
                    """
                    p_cur.execute(insert_query, (row['timestamp'], row['val'], row['increment'] ))# 使用 MySQL 里的原始时间戳
                    
                    
                    monitor_stats["last_synced_id"] = row['id']
                    monitor_stats["sync_count"] += 1
                
                p_conn.commit()
                p_cur.close()
                p_conn.close()
            
            m_cur.close()
            m_conn.close()
        except Exception as e:
            print(f"同步报错: {e}")
        
        time.sleep(1)


# --- 启动监控线程 ---
# daemon=True 意味着当主程序关闭时，监控线程也会跟着关闭
threading.Thread(target=start_monitoring, daemon=True).start()

# --- API 路由 ---
@app.get("/")
def check_status():
    return {
        "title": "MySQL -> PostgreSQL 自动同步监控中",
        "current_stats": monitor_stats,
        "next_step": "去 PHPMyAdmin 插入新数据，然后回来刷新这个页面看看"
    }
