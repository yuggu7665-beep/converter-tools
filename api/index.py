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

from mangum import Mangum
from api.main import app

# Vercel requires ASGI handler via Mangum
handler = Mangum(app, lifespan="off")
