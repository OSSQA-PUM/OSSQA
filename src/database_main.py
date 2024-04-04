from database.server import create_app

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run(port=5080, host='0.0.0.0')
