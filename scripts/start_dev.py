"""Launch script to start both FastAPI Backend (port 8000) and Next.js Frontend (port 3000) simultaneously."""

import sys
import subprocess
import time
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

def main():
    print("=" * 60)
    print("Starting Nagpur Krishi Data (नागपूर शेती आकडे)")
    print("=" * 60)

    # 1. Start FastAPI backend
    print("[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    api_cmd = [sys.executable, "-m", "uvicorn", "apps.api.src.main:app", "--host", "127.0.0.1", "--port", "8000"]
    api_proc = subprocess.Popen(api_cmd, cwd=str(ROOT_DIR))

    # Give backend a moment to boot
    time.sleep(2)

    # 2. Start Next.js frontend
    print("[2/2] Starting Next.js Web App on http://localhost:3000 ...")
    web_dir = ROOT_DIR / "apps" / "web"
    is_windows = sys.platform == "win32"
    npm_cmd = "npm.cmd" if is_windows else "npm"
    web_proc = subprocess.Popen([npm_cmd, "run", "dev"], cwd=str(web_dir))

    print("\n" + "=" * 60)
    print("SUCCESS! Both services are now running:")
    print("  • Web App:     http://localhost:3000")
    print("  • Backend API: http://127.0.0.1:8000")
    print("  • API Docs:    http://127.0.0.1:8000/docs")
    print("Press Ctrl+C to stop both servers.")
    print("=" * 60 + "\n")

    try:
        while True:
            time.sleep(1)
            if api_proc.poll() is not None:
                print("Backend terminated unexpectedly.")
                break
            if web_proc.poll() is not None:
                print("Frontend terminated unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        api_proc.terminate()
        web_proc.terminate()
        print("All servers stopped cleanly.")

if __name__ == "__main__":
    main()
