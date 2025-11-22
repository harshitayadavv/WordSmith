"""
WordSmith Backend Runner
Run this script to start the FastAPI server
"""
import uvicorn
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Check if running in production (Render sets RENDER=true)
    is_production = os.environ.get("RENDER", False)
    
    print("🚀 Starting WordSmith Backend...")
    print(f"📚 API Documentation will be available at: http://localhost:{port}/docs")
    print(f"🔍 Health Check: http://localhost:{port}/api/v1/health")
    print("⚡ Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Changed from 127.0.0.1
        port=port,       # Changed from 8000
        reload=not is_production,  # Disable reload in production
        log_level="info"
    )