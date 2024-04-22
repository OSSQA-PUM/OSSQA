"""
The entry point of the backend.
"""
import server


if __name__ == "__main__":
    app = server.create_app()
    app.run(port=5090, host='0.0.0.0')
