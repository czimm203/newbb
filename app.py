from datetime import datetime, timedelta
from flask import Flask, render_template, request
from pathlib import Path
from newbb import db

name = Path(__file__).parent.name.capitalize()
app = Flask(__name__)
#
@app.route("/")
def index():
    rows = db.select_data()
    modded_rows = []
    for row in rows:
        d = {k:row[k] for k in row.keys()}
        dt = datetime.strptime(d["date"],"%Y-%m-%dT%H:%M")
        d['date'] = dt.strftime("%m/%d %H:%M")
        modded_rows.append(d)
    next_feed_dt = datetime.strptime(modded_rows[0]['date'], "%m/%d %H:%M")
    next_feed = (next_feed_dt + timedelta(hours=2)).strftime("%m/%d %H:%M")
    return render_template("index.html", name = name, rows = modded_rows,
                           marker = (" ","\u2705"), next_feed = next_feed)

@app.route("/report/")
def report():
    return render_template("report.html", name = name)

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

    for item in form.items():
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
    db.insert_data(row)
    return render_template("submission.html", name = name)

if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=False)
