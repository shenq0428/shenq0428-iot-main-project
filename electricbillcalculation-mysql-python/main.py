import threading
import time
import subprocess
import sys
import os

def run_background_script(script_name, interval):
    """用于运行需要持续循环的脚本"""
    print(f"🟢 [后台启动] {script_name} (执行频率: {interval}秒)")
    while True:
        try:
            # 使用 subprocess 运行脚本，确保它能独立执行
            subprocess.run([sys.executable, script_name])
        except Exception as e:
            print(f"❌ {script_name} 出错: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    print("=== ⚡ 电费管理系统控制中心 ===")
    
    # 定义任务：(脚本名, 间隔秒数)
    tasks = [
        ("power_reading.py", 60),           # 每60秒采集一次原始数据
        ("electricity_usage_difference.py", 300) # 每5分钟计算一次分类差值
    ]

    # 启动后台线程
    for script, sec in tasks:
        t = threading.Thread(target=run_background_script, args=(script, sec), daemon=True)
        t.start()

    print("\n✅ 模拟器和分析器已在后台运行。")
    print("👉 输入 'calc'：立即计算并更新今日账单 (Total Cost)")
    print("👉 输入 'exit'：关闭所有任务并退出")

    try:
        while True:
            cmd = input("\n请输入指令: ").strip().lower()
            if cmd == 'calc':
                print("💰 正在执行一次性结算...")
                subprocess.run([sys.executable, "electricity_total_cost.py"]) #
            elif cmd == 'exit':
                print("👋 正在关闭系统...")
                subprocess.run([sys.executable, "electricity_total_cost.py"])
                print("✅ Final settlement complete. System shutting down.")
                break
            else:
                print("❓ 未知指令，请输入 'calc' 或 'exit'")
    except KeyboardInterrupt:
        print("\n👋 强制退出")
        subprocess.run([sys.executable, "electricity_usage_difference.py"])
        subprocess.run([sys.executable, "electricity_total_cost.py"])
        print("✅ 结算完成，系统安全退出。")