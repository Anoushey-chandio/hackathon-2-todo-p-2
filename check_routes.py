import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from src.main import app
    print("Routes registered in app:")
    for route in app.routes:
        print(f"Path: {route.path}, Name: {route.name}, Methods: {getattr(route, 'methods', 'N/A')}")
except Exception as e:
    print(f"Error: {e}")
