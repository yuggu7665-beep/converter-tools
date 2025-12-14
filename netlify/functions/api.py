"""
Netlify Function - API Handler
Wraps the FastAPI application for serverless deployment
"""
from mangum import Mangum
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), '../../backend')
sys.path.insert(0, backend_dir)

from api.main import app

# Create Mangum handler for Netlify Functions
handler = Mangum(app, lifespan="off")
