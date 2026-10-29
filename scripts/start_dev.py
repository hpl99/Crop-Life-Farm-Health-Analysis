"""Launch script to start both FastAPI Backend (port 8000) and Next.js Frontend (port 3000) simultaneously."""

import sys
import subprocess
import time
import os
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parents[1]

def free_port(port: int):
    """Ensure port is not held by a stale background process."""
    if sys.platform == "win32":
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", f"(Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue).OwningProcess"],
                capture_output=True, text=True
            )
            for line in res.stdout.strip().splitlines():
                pid_str = line.strip()
                if pid_str and pid_str != "0" and pid_str.isdigit() and int(pid_str) != os.getpid():
                    subprocess.run(["taskkill", "/F", "/PID", pid_str], capture_output=True)
        except Exception:
            pass

def main():
    print("=" * 60)
    print("Starting Nagpur Krishi Data (Nagpur Sheti Aakade)")
    print("=" * 60)

    # Free any lingering processes on ports 8000 and 3000
    free_port(8000)
    free_port(3000)
    time.sleep(1.0)  # Allow Windows TCP socket cleanup time

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # 1. Start FastAPI backend
    print("[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    api_cmd = [sys.executable, "-m", "uvicorn", "apps.api.src.main:app", "--host", "127.0.0.1", "--port", "8000"]
    api_proc = subprocess.Popen(api_cmd, cwd=str(ROOT_DIR), env=env)

    # Wait for backend health probe
    import urllib.request
    backend_ready = False
    for attempt in range(15):
        time.sleep(0.5)
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/healthz", timeout=1) as resp:
                if resp.status == 200:
                    backend_ready = True
                    print("       Backend verified ready on port 8000!")
                    break
        except Exception:
            pass

    if not backend_ready:
        print("WARNING: Backend health check did not return 200 within 7.5s, proceeding anyway...")

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

