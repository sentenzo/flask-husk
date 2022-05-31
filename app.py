import os
from flask import Flask, render_template, request
from time import sleep
from random import random

from db import DB

DBG = os.environ.get("DBG", "0") == "1"


def dbg_rand_sleep(a=0.1, b=0.8):
    if DBG:
        d = b - a
        if d > 0:
            sleep(random()*d + a)
        return


app = Flask(__name__)
app.secret_key = os.urandom(24)


db = DB()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax/get_counter", methods=["GET"])
def ajax_get_counter():
    dbg_rand_sleep()
    return {"counter": db.get_counter()}


@app.route("/ajax/inc_counter", methods=["POST"])
def ajax_inc_counter():
    dbg_rand_sleep()
    diff = 1
    if "diff" in request.form:
        diff = int(request.form.get('diff'))
    db.inc_counter(diff)
    return {"counter": db.get_counter()}


if __name__ == "__main__":
    app.run()
