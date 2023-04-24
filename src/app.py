from flask import Flask, send_file
from database.dapi import DatabaseConnector


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return '<h1>It works!<h1>'


@app.route("/download/<book_id>")
def download_book_stats(book_id):
    filename = DatabaseConnector.borrows_to_file(book_id)
    return send_file(filename)


if __name__ == "__main__":
    app.run("0.0.0.0")
