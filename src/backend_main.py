"""
This is the main entry point for the backend of the application.

It creates an instance of the Flask app using the `create_app()` function
from the `backend.server` module, and then runs the app on port 5090,
allowing connections from any host.

Usage:
    python backend_main.py
"""
import backend.server as server


if __name__ == "__main__":
    app = server.create_app()
    app.run(port=5090, host='0.0.0.0')
