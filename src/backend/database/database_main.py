from server import create_app

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run(port=5090, host='0.0.0.0')