import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

# 加载 .env 配置
load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

def run_realtime_analysis():
    print("🚀 启动自动化电量差值分析系统...")
    
    while True:
        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # 1. 获取过去 24 小时的原始数据 (修改表名为 power_reading)
            query = """
                SELECT 
                    FROM_UNIXTIME(CEIL(UNIX_TIMESTAMP(timestamp) / 300) * 300) AS window_end_time,
                    SUM(increment) as total_growth
                FROM power_reading
                WHERE timestamp >= NOW() - INTERVAL 24 HOUR
                GROUP BY window_end_time
            """
            cursor.execute(query)
            
            data_map = {
                row[0].strftime('%Y-%m-%d %H:%M:00'): row[1] 
                for row in cursor.fetchall()
            }

            # 2. 构造 5 分钟间隔的时间轴
            now = datetime.now()
            end_node = now.replace(second=0, microsecond=0)
            # 向上取整到最近的 5 分钟
            end_node += timedelta(minutes=(5 - end_node.minute % 5) if end_node.minute % 5 != 0 else 5)

            batch_data = []
            for i in range(288): # 24小时，共288个点
                slot_dt = end_node - timedelta(minutes=i * 5)
                current_slot = slot_dt.strftime('%Y-%m-%d %H:%M:00')
                net_diff = max(0, float(data_map.get(current_slot, 0)))
                
                # 为 SQL 准备 4 个参数: window_end_time, net_diff, 以及两次用于判定时间的 current_slot
                batch_data.append((current_slot, net_diff, current_slot, current_slot))

            # 3. 动态匹配价格表描述并插入 (修改表名为 electricity_usage_difference 和 electricity_price_range)
            insert_sql = """
                REPLACE INTO electricity_usage_difference (window_end_time, net_diff, morning_night) 
                VALUES (
                    %s, 
                    %s, 
                    (SELECT description 
                     FROM electricity_price_range 
                     WHERE TIME(%s) > start_time AND TIME(%s) <= end_time 
                     LIMIT 1)
                )
            """

            cursor.executemany(insert_sql, batch_data)
            
            connection.commit()
            print(f"📊 分析成功: {now.strftime('%H:%M:%S')} | 已根据 electricity_price_range 自动分类")

        except Error as e:
            print(f"❌ 数据库错误: {e}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
        
        # 每 5 分钟同步一次
        time.sleep(300)

if __name__ == "__main__":
    run_realtime_analysis()