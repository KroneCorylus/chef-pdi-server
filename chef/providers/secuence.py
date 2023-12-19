
import sqlite3
from datetime import datetime, timezone


def insert(secuence_name: str) -> int:
    connection = sqlite3.connect('chef.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO secuence_execution (secuence_name,init_date) VALUES (?,?)",
        (secuence_name, datetime.now(timezone.utc))
    )
    rowid = cursor.lastrowid or -1
    connection.commit()
    cursor.close()
    connection.close()
    return rowid


def update_end_date(rowid: int) -> int:
    connection = sqlite3.connect('chef.db')
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE secuence_execution SET end_date = ? WHERE rowid = ?",
        (datetime.now(timezone.utc), rowid)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return rowid
