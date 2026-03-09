import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_database():
    # Credentials from .env
    config = {
        'host': os.getenv("DB_HOST"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASS"),
        'database': os.getenv("DB_NAME")
    }

    # Order is important due to logic flow
    sql_files = [
        "mysqldatabase-create/power_reading.sql",
        "mysqldatabase-create/electricity_price_range.sql",
        "mysqldatabase-create/electricity_usage_difference.sql",
        "mysqldatabase-create/electricity_total_cost.sql"
    ]

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print(f"🔗 Connected to database: {config['database']}")

        for file_path in sql_files:
            if os.path.exists(file_path):
                print(f"📖 Importing {file_path}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Split by semicolon to execute multiple statements in one file
                    sql_commands = f.read().split(';')
                    for command in sql_commands:
                        if command.strip():
                            cursor.execute(command)
                print(f"✅ {file_path} imported successfully.")
            else:
                print(f"⚠️ Warning: {file_path} not found.")

        conn.commit()
        print("\n✨ Database initialization complete!")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    initialize_database()