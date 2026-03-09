import mysql.connector
from mysql.connector import Error
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

def run_cost_calculation():
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # 核心 SQL 修改点：替换为新的表名
        # electricity_usage_difference (输入) -> electricity_total_cost (输出)
        calculation_query = """
            SELECT 
                CASE 
                    WHEN TIME(d.window_end_time) >= '00:00:00' AND TIME(d.window_end_time) <= '08:00:00'
                    THEN DATE_SUB(DATE(d.window_end_time), INTERVAL 1 DAY)
                    ELSE DATE(d.window_end_time)
                END as logic_date,
                -- 1. 计算总量
                SUM(CASE WHEN d.morning_night = 'morning' THEN d.net_diff ELSE 0 END) as total_morning_diff,
                SUM(CASE WHEN d.morning_night = 'night' THEN d.net_diff ELSE 0 END) as total_night_diff,
                -- 2. 计算金额
                SUM(CASE WHEN d.morning_night = 'morning' THEN d.net_diff * p.price ELSE 0 END) as day_cost,
                SUM(CASE WHEN d.morning_night = 'night' THEN d.net_diff * p.price ELSE 0 END) as night_cost,
                SUM(d.net_diff * p.price) as total_cost
            FROM electricity_usage_difference d
            JOIN (
                SELECT DISTINCT description, price FROM electricity_price_range
            ) p ON d.morning_night = p.description
            GROUP BY logic_date
            ORDER BY logic_date ASC
        """
           
        print("💰 正在进行每日成本核算...")
        cursor.execute(calculation_query)
        results = cursor.fetchall()

        if not results:
            print("⚠️ 没有找到可计算的差值数据。")
            return

        # 更新插入逻辑，对应 electricity_total_cost 表
        delete_sql = "DELETE FROM electricity_total_cost WHERE log_date = %s"
        insert_sql = """
            INSERT INTO electricity_total_cost 
            (log_date, total_morning_diff, total_night_diff, day_cost, night_cost, total_cost) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        print("-" * 110)
        print(f"{'日期':<12} | {'早班总量':<10} | {'晚班总量':<10} | {'早班金额':<10} | {'晚班金额':<10} | {'总金额':<10}")
        print("-" * 110)

        for row in results:
            log_date, t_m_diff, t_n_diff, day_cost, night_cost, total_cost = row
            
            # 清理并同步数据
            cursor.execute(delete_sql, (log_date,))
            cursor.execute(insert_sql, (log_date, t_m_diff, t_n_diff, day_cost, night_cost, total_cost))
            
            print(f"{str(log_date):<12} | {t_m_diff:10.2f} | {t_n_diff:10.2f} | {day_cost:10.2f} | {night_cost:10.2f} | {total_cost:10.2f}")

        connection.commit()
        print("-" * 110)
        print("🚀 结算完成！数据已更新至 electricity_total_cost 表。")

    except Error as e:
        print(f"❌ 数据库错误: {e}")
        if connection: connection.rollback()
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    run_cost_calculation()