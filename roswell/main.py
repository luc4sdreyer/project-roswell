import click
from flask import Flask

app = Flask(__name__)


@app.route("/api/")
def api():
    return "Hello world"


def cli(host, port, debug):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    cli("0.0.0.0", 8080, True)
