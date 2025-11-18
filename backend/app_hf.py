"""
Hugging Face Spaces deployment configuration
This file is used when deploying to Hugging Face Spaces
"""
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
from app.main import app

# Hugging Face Spaces expects the app to be available as 'app'
# This file serves as the entry point for HF Spaces
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (HF Spaces sets this)
    port = int(os.environ.get("PORT", 7860))
    
    print(f"🚀 Starting WordSmith Backend on Hugging Face Spaces (Port: {port})")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )