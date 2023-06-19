from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/report/")
def report():
    return render_template("report.html")

@app.route("/report/submit", methods = ["POST"])
def submit_report():
    print(request.form)
    return render_template("submission.html")
