


import subprocess
import sys
import time
import os

# Create folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("vector_db", exist_ok=True)

print("=" * 50)
print("📚 Starting Book Chatbot")
print("=" * 50)

# Start backend
print("\n📡 Starting backend server...")
backend = subprocess.Popen([
    sys.executable, "-m", "uvicorn",
    "backend:app",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--reload"
])

time.sleep(3)

# Start frontend
print("🎨 Starting frontend...")
frontend = subprocess.Popen([
    sys.executable, "-m", "streamlit",
    "run", "frontend.py",
    "--server.port", "8501"
])

print("\n✅ Everything is running!")
print("📱 Frontend: http://localhost:8501")
print("🔧 Backend API: http://localhost:8000")
print("📖 API Docs: http://localhost:8000/docs")
print("\nPress Ctrl+C to stop\n")

# Wait for processes
try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    backend.terminate()
    frontend.terminate()


