import server

if __name__ == "__main__":
    app = server.create_app()
    app.debug = True
    app.run(port=5080, host='0.0.0.0')
