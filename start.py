#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    port = os.environ.get("PORT", "8501")
    print(f"Starting Umrah Planner AI on port {port}...")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--server.fileWatcherType", "none"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
