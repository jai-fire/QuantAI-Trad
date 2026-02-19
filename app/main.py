import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.service import run_service

print("🚀 PRO TRADING PLATFORM STARTED")

run_service()
