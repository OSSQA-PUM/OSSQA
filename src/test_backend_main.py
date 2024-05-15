"""
This script starts a test server for the backend application.

Usage:
    python test_backend_main.py

The server runs on port 5091 by default.
"""
import backend.server as server


if __name__ == "__main__":
    app = server.create_test_app()
    app.run(port=5091)
