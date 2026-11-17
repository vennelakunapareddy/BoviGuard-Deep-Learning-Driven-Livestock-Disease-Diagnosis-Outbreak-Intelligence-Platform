import os
import sys
import time
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', write_through=True)

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
ML_DIR = ROOT / "ml-service"
FRONTEND_DIR = ROOT / "frontend" if (ROOT / "frontend").exists() else ROOT / "frontend-v2"

def free_port(port):
    if os.name == 'nt':
        try:
            netstat_exe = r"C:\Windows\System32\netstat.exe"
            taskkill_exe = r"C:\Windows\System32\taskkill.exe"
            cmd = f'"{netstat_exe}" -ano'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
            lines = output.strip().split('\n')
            for line in lines:
                if f":{port} " in line or f":{port}\t" in line:
                    parts = line.strip().split()
                    if len(parts) >= 5 and 'LISTENING' in line:
                        pid = parts[-1]
                        if pid.isdigit() and int(pid) > 0:
                            subprocess.call(f'"{taskkill_exe}" /F /PID {pid}', shell=True)
        except Exception:
            pass

def launch_system():
    print("==================================================", flush=True)
    print("=== LAUNCHING ALL 3 SUB-SERVICES SIMULTANEOUSLY ===", flush=True)
    print("==================================================", flush=True)

    free_port(3000)
    free_port(5000)
    free_port(5173)

    # 1. Express Backend
    print("\n[1/3] Launching Express Backend Server (Port 3000)...", flush=True)
    backend_proc = subprocess.Popen(
        ["node", "server.js"],
        cwd=str(BACKEND_DIR),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    time.sleep(3)
    print(f"[OK] Express Backend Server running (PID: {backend_proc.pid})", flush=True)

    # 2. FastAPI ML Service
    print("\n[2/3] Launching Python FastAPI ML Microservice (Port 5000)...", flush=True)
    ml_python = ML_DIR / "venv" / "Scripts" / "python.exe"
    python_exe = sys.executable
    if ml_python.exists():
        try:
            subprocess.check_call([str(ml_python), "-c", "import torch, fastapi, uvicorn"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            python_exe = str(ml_python)
        except Exception:
            python_exe = sys.executable
    ml_proc = subprocess.Popen(
        [python_exe, "app.py"],
        cwd=str(ML_DIR),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    time.sleep(4)
    print(f"[OK] FastAPI ML Microservice running (PID: {ml_proc.pid})", flush=True)

    # 3. Vite Frontend Server (Port 5173)
    print("\n[3/3] Launching Vite Frontend Server (Port 5173)...", flush=True)
    npx_cmd = "npx.cmd" if os.name == 'nt' else "npx"
    frontend_proc = subprocess.Popen(
        [npx_cmd, "vite", "--port", "5173", "--host"],
        cwd=str(FRONTEND_DIR),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    time.sleep(4)
    print(f"[OK] Vite Frontend Application running (PID: {frontend_proc.pid})", flush=True)

    print("\n==================================================", flush=True)
    print("=== ALL 3 SERVICES ARE RUNNING AT THE SAME TIME! ===", flush=True)
    print("Frontend Web App:    http://localhost:5173", flush=True)
    print("Express Backend API: http://localhost:3000", flush=True)
    print("FastAPI ML Service:  http://localhost:5000", flush=True)
    print("==================================================", flush=True)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_proc.terminate()
        ml_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    launch_system()
