import os
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

counter = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax/get_counter", methods=["GET"])
def ajax_get_counter():
    return {"counter": counter}  # f"{{counter: {counter}}}"


@app.route("/ajax/inc_counter", methods=["POST"])
def ajax_inc_counter():
    global counter
    diff = request.form.get('diff')
    counter += diff or 1
    return "{}"


if __name__ == "__main__":
    app.run()
