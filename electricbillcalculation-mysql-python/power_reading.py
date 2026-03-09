import mysql.connector
import time
import os
from dotenv import load_dotenv

# 加载 .env 文件中的变量
load_dotenv()

def get_db_connection():
    """获取数据库连接"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

def insert_power_reading(cursor, val, increment):
    """
    将模拟数据存入 power_reading 表
    """
    # 统一使用你 SQL 文件中的表名
    sql = "INSERT INTO power_reading (val, increment) VALUES (%s, %s)"
    cursor.execute(sql, (val, increment))

def main():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        t3_old_value, t3_new_value = 0, 1
        t3_last_recorded_value = 0
        count = 0 

        print("🚀 Data simulation service is running...")
        
        while True:
            t3_value = t3_old_value + t3_new_value
            increment = t3_value - t3_last_recorded_value

            # 执行插入逻辑
            insert_power_reading(cursor, t3_value, increment)

            # 更新迭代变量
            t3_old_value, t3_new_value = t3_new_value, t3_value
            t3_last_recorded_value = t3_value

            connection.commit()
            count += 1
            print(f"📊 [{count}] Saved: Total={t3_value}, Inc={increment}")
            
            time.sleep(60) 
    
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()