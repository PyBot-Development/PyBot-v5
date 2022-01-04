from flask import Flask, Response
import os
import support
import threading

class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    app = Flask(__name__)
    def getFile(filename):
        try:
            src = f"{support.path}/{filename}"
            return open(src).read()
        except IOError as exc:
            return str(exc)

    @app.route('/')
    def index(self):
        return Response(self.getFile("data/web/index.html"), mimetype="text/html")

    @app.route('/index.css')
    def css(self):
        return Response(self.getFile("data/web/index.css"), mimetype="text/html")

    @app.route('/bootstrap.css')
    def bootstrap(self):
        return Response(self.getFile("data/web/bootstrap-5.1.3-dist/css/bootstrap.min.css"), mimetype="text/html")


    if __name__ == "__main__":
        app.run(debug=support.config.get("debug"))