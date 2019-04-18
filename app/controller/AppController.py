from flask import request, render_template
from app import app
from app.constant import RequestMethod


@app.route("/", methods=RequestMethod.GET)
def index():
    return render_template("index.html")
