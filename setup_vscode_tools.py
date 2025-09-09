#!/usr/bin/env python3
"""
Simple VS Code Tools Setup for L.I.F.E. Autonomous Optimizer
Copyright Sergio Paya Borrull 2025. All Rights Reserved.
"""

import json
from pathlib import Path


def setup_vscode_tools():
    """Set up VS Code tools for autonomous optimizer development"""
    print("🧠 Setting up VS Code Tools for L.I.F.E. Autonomous Optimizer")
    print("=" * 60)

    workspace_root = Path(__file__).parent
    vscode_dir = workspace_root / ".vscode"
    vscode_dir.mkdir(exist_ok=True)

    # Create VS Code snippets for L.I.F.E. development
    snippets = {
        "L.I.F.E. Optimizer Debug": {
            "prefix": "life-debug",
            "body": [
                "# L.I.F.E. Autonomous Optimizer Debug",
                "import logging",
                "logging.basicConfig(level=logging.DEBUG)",
                "logger = logging.getLogger(__name__)",
                "",
                "# Debug autonomous optimization cycle",
                "state = await autonomous_optimizer.autonomous_optimization_cycle(neural_data)",
                "logger.debug(f'Optimization state: {state}')",
            ],
            "description": "L.I.F.E. autonomous optimizer debug snippet",
        },
        "SOTA Performance Test": {
            "prefix": "sota-test",
            "body": [
                "# SOTA Performance Validation",
                "def test_sota_performance():",
                "    targets = {'latency_ms': 15.12, 'accuracy': 0.959}",
                "    # Test implementation",
                "    assert actual_latency <= targets['latency_ms']",
                "    assert actual_accuracy >= targets['accuracy']",
                "    print('🏆 SOTA Performance Achieved!')",
            ],
            "description": "SOTA performance test template",
        },
    }

    snippets_file = vscode_dir / "python.json"
    with open(snippets_file, "w") as f:
        json.dump(snippets, f, indent=2)
    print(f"✅ Created snippets: {snippets_file}")

    # Update launch.json with debugpy (modern Python debugger)
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "🧠 Debug Autonomous Optimizer",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceFolder}/autonomous_optimizer.py",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "env": {"PYTHONPATH": "${workspaceFolder}", "DEBUG_MODE": "true"},
                "justMyCode": False,
                "stopOnEntry": False,
                "showReturnValue": True,
            },
            {
                "name": "⚡ Debug Model Optimizer",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceFolder}/model_optimizer.py",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "justMyCode": False,
            },
            {
                "name": "🏆 Debug SOTA Benchmarks",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceFolder}/sota_benchmark.py",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "justMyCode": False,
            },
        ],
    }

    launch_file = vscode_dir / "launch.json"
    with open(launch_file, "w") as f:
        json.dump(launch_config, f, indent=2)
    print(f"✅ Updated launch config: {launch_file}")

    # Create simple performance monitor
    perf_monitor = workspace_root / "quick_monitor.py"
    monitor_code = '''#!/usr/bin/env python3
"""Quick performance monitor for L.I.F.E. optimization"""

import psutil
import time
from datetime import datetime

def monitor():
    print("🔍 L.I.F.E. Performance Monitor (Press Ctrl+C to stop)")
    print("-" * 50)
    
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            print(f"\\r{datetime.now().strftime('%H:%M:%S')} | "
                  f"CPU: {cpu:5.1f}% | "
                  f"RAM: {memory.percent:5.1f}% | "
                  f"Available: {memory.available // (1024**3)}GB", end="")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Monitoring stopped")

if __name__ == "__main__":
    monitor()
'''

    with open(perf_monitor, "w") as f:
        f.write(monitor_code)
    print(f"✅ Created monitor: {perf_monitor}")

    # Create quick test runner
    test_runner = workspace_root / "quick_test.py"
    test_code = '''#!/usr/bin/env python3
"""Quick test runner for L.I.F.E. optimization"""

import subprocess
import sys
from pathlib import Path

def run_tests():
    print("🧪 L.I.F.E. Quick Test Runner")
    print("-" * 40)
    
    test_files = [
        "test_autonomous_optimizer.py",
        "test_model_optimizer.py"
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"\\n🔬 Testing {test_file}...")
            try:
                result = subprocess.run([sys.executable, test_file], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"✅ {test_file} PASSED")
                else:
                    print(f"❌ {test_file} FAILED")
                    if result.stderr:
                        print(f"   Error: {result.stderr[:200]}...")
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file} TIMEOUT")
            except Exception as e:
                print(f"💥 {test_file} ERROR: {e}")
        else:
            print(f"⚠️ {test_file} not found")
    
    print("\\n🎯 Testing complete!")

if __name__ == "__main__":
    run_tests()
'''

    with open(test_runner, "w") as f:
        f.write(test_code)
    print(f"✅ Created test runner: {test_runner}")

    print("\n✅ VS Code Tools Setup Complete!")
    print("\n📁 Created Files:")
    print("   🐛 .vscode/launch.json - Debug configurations")
    print("   ✂️ .vscode/python.json - Code snippets")
    print("   📊 quick_monitor.py - Performance monitoring")
    print("   🧪 quick_test.py - Test runner")
    print("\n🚀 Usage:")
    print("   • Press F5 to debug autonomous optimizer")
    print("   • Type 'life-debug' for debug snippets")
    print("   • Run 'python quick_monitor.py' for monitoring")
    print("   • Run 'python quick_test.py' for testing")


if __name__ == "__main__":
    setup_vscode_tools()
