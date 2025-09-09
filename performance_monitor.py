#!/usr/bin/env python3
"""
Quick Performance Monitor for L.I.F.E. Autonomous Optimizer
Real-time system monitoring during optimization
"""

import time
from datetime import datetime

import psutil


def monitor():
    """Monitor system performance in real-time"""
    print("🔍 L.I.F.E. Performance Monitor")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 50)

    try:
        start_time = time.time()

        while True:
            # Get system metrics
            cpu = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Check for autonomous optimizer process
            optimizer_running = False
            optimizer_cpu = 0
            optimizer_memory = 0

            for proc in psutil.process_iter(
                ["pid", "name", "cmdline", "cpu_percent", "memory_percent"]
            ):
                try:
                    cmdline = " ".join(proc.info["cmdline"] or [])
                    if "autonomous_optimizer.py" in cmdline:
                        optimizer_running = True
                        optimizer_cpu = proc.info["cpu_percent"] or 0
                        optimizer_memory = proc.info["memory_percent"] or 0
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Display metrics
            uptime = time.time() - start_time
            print(
                f"\r{datetime.now().strftime('%H:%M:%S')} | "
                f"Uptime: {uptime:6.0f}s | "
                f"CPU: {cpu:5.1f}% | "
                f"RAM: {memory.percent:5.1f}% | "
                f"Free: {memory.available // (1024**3):2.0f}GB",
                end="",
            )

            if optimizer_running:
                print(
                    f" | 🧠 Optimizer: CPU {optimizer_cpu:4.1f}% RAM {optimizer_memory:4.1f}%",
                    end="",
                )
            else:
                print(" | 🧠 Optimizer: Not Running", end="")

            # Flush output
            print("", flush=True, end="")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Performance monitoring stopped")
        print(f"📊 Total monitoring time: {time.time() - start_time:.1f} seconds")


def monitor_brief():
    """Brief performance check"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    print(f"💻 System Status:")
    print(f"   CPU Usage: {cpu:.1f}%")
    print(f"   Memory Usage: {memory.percent:.1f}%")
    print(f"   Available RAM: {memory.available // (1024**3):.1f}GB")

    # Check if Python processes are consuming resources
    python_processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            if "python" in proc.info["name"].lower():
                python_processes.append(
                    {
                        "pid": proc.info["pid"],
                        "cpu": proc.info["cpu_percent"] or 0,
                        "memory": proc.info["memory_percent"] or 0,
                    }
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if python_processes:
        print(f"🐍 Python Processes: {len(python_processes)}")
        for proc in sorted(python_processes, key=lambda x: x["cpu"], reverse=True)[:3]:
            print(
                f"   PID {proc['pid']}: CPU {proc['cpu']:.1f}% RAM {proc['memory']:.1f}%"
            )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--brief":
        monitor_brief()
    else:
        monitor()
