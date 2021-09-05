from flask import Flask
from db_manager import connect

app = Flask(__name__)



@app.route("/")
def index():
    cursor = connect()
    return "<p>Index Page</p>"


if __name__ == "__main__":
    connect()