"""
Vercel Serverless Function - API Handler
"""
import sys
import os
from pathlib import Path

# Add backend to path
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent / "backend"
sys.path.insert(0, str(backend_dir))

from api.main import app

# Vercel handler
handler = app
