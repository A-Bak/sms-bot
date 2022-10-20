from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    app.logger.info("Started SMS-Bot.")
    return "<p>Hello, this is SMS-Bot!</p>"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
