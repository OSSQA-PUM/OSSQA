"""
The entry point of the backend.
"""
import backend.server as server


if __name__ == "__main__":
    app = server.create_test_app()
    app.run(port=5091)
