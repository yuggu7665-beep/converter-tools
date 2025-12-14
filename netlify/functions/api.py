"""
Netlify Function - API Handler
Wraps the FastAPI application for serverless deployment
"""
import sys
import os
from pathlib import Path

# Get the absolute path to backend directory
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import after path is set
from mangum import Mangum
from api.main import app

# Create Mangum handler for Netlify Functions
handler = Mangum(app, lifespan="off")
