"""
Application entry point
"""
import os
from dotenv import load_dotenv
import uvicorn
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment or default to development
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    
    # Check if using real X API
    twitter_token = os.getenv('TWITTER_BEARER_TOKEN')
    if twitter_token:
        print("✅ X API Bearer Token detected - Using REAL X API v2")
        print(f"   Token: {twitter_token[:20]}...{twitter_token[-10:]}")
    else:
        print("ℹ️  No Bearer Token found - Using Mock Service")
    
    print(f"\n🚀 Starting server on http://0.0.0.0:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"📖 Alternative Docs: http://localhost:{port}/redoc")
    print(f"\n📍 Test endpoints:")
    print(f"   curl http://localhost:{port}/hashtags/python?limit=5")
    print(f"   curl http://localhost:{port}/users/twitter?limit=5")
    print()
    
    uvicorn.run(
        "run:app",
        host='0.0.0.0',
        port=port,
        reload=True if config_name == 'development' else False
    )
