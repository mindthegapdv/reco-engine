# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")

def hello():
    return "Hello World!"


@app.route("/test")
def test():
    return "meow"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)