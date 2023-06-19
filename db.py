import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class Row:
    date: str = datetime.now().strftime("%Y-%m-%dT%H:%M")
    poo: bool = False
    pee: bool = False
    feeding: bool = False
    amount: int = 0
    pump: bool = False
    id: int | None = None

def create_row(data: dict[str, Any]) -> Row:
    print(data)
    return Row(
                date = data["date"],
                poo = data["poo"],
                pee = data["pee"],
                feeding = data["feeding"],
                pump = data["pump"],
                amount = data["amount"],
                id = data["id"] 
            )

def init_db():
    with sqlite3.connect("./data.db") as conn:
        with open("./migrations/init.sql") as f:
            conn.executescript(f.read())
            conn.commit()

def get_db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

def select_data(limit = 20) -> list[sqlite3.Row]:
    conn = get_db_connect()
    cur = conn.cursor()
    sql = """
        SELECT * FROM data ORDER BY date DESC LIMIT ?;
    """
    cur.execute(sql, (str(limit),))
    res = cur.fetchall()
    print(res[-1]['feeding'])
    conn.close()
    return res

def insert_data(data: Row):
    conn = get_db_connect()
    sql = """
        INSERT INTO data(date, poo, pee, feeding, amount, pump)
        VALUES(?,?,?,?,?,?);
    """
    conn.execute(sql, (data.date, data.poo, data.pee,
                 data.feeding, data.amount, data.pump))
    conn.commit()
    conn.close()
