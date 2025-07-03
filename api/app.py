import sys
import os

# Add the parent directory to the path so we can import from the main app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def handler(request):
    """Vercel handler function"""
    return app(request.environ, request.start_response)

if __name__ == "__main__":
    app.run(debug=True)