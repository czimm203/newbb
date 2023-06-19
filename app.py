from datetime import datetime
from flask import Flask, render_template, request
from . import db

# db.init_db()
app = Flask(__name__)

@app.route("/")
def index():
    rows = db.select_data()
    print(rows)
    return render_template("index.html", rows = rows, marker = (" ","\u2705"))

@app.route("/report/")
def report():
    return render_template("report.html")

@app.route("/report/submit", methods = ["POST"])
def submit_report():
    form = request.form
    data = {
                'id': None,
                'date': datetime.now().strftime("%Y-%m-%dT%H:%M"),
                'poo': False,
                'pee': False,
                'feeding': False,
                'amount': 0,
                'pump': False,
            }

    print(form)
    for item in form.items():
        print(item)
        match item:
            case ['id', i] if id != None:
                data["id"] = int(i)
            case ['time', t] if t != '':
                data["date"] = t #if t != '' else datetime.now().strftime("%Y-%m-%dT%H:%M")
            case ['poo', _]:
                data["poo"] = True
            case ['pee', _]:
                data["pee"] = True
            case 'feeding', _:
                data["feeding"] = True
            case ['amount', a] if a != '':
                data["amount"] = int(a)
            case 'pump', _:
                data["pump"] = True

    row = db.create_row(data)
    print(row)
    db.insert_data(row)
    return render_template("submission.html")
