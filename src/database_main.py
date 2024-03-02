from database.server import *

if __name__ == "__main__":
    app.debug = True
    app.run(port=5080)
