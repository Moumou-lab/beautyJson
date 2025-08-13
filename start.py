import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# 启动后端
print("[INFO] 启动后端 Flask...")
backend_proc = subprocess.Popen(
    [sys.executable, "server.py"],
    cwd=BACKEND_DIR
)

# 等待后端端口监听
time.sleep(2)

# 启动前端静态服务器（Python 内置）
print("[INFO] 启动前端静态服务器 (http://localhost:8080/frontend/index.html)...")
frontend_proc = subprocess.Popen(
    [sys.executable, "-m", "http.server", "8080"],
    cwd=BASE_DIR
)

print("[INFO] 前后端已启动。按 Ctrl+C 停止。")

try:
    backend_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print("\n[INFO] 正在停止服务...")
    backend_proc.terminate()
    frontend_proc.terminate()
