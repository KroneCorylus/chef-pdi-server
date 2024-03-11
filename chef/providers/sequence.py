
import sqlite3
from datetime import datetime, timezone

from config import LOG_RETENTION


def insert(sequence_name: str) -> int:
    connection = sqlite3.connect('chef.db')
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO
            sequence_execution (sequence_name,init_date)
        VALUES (?,?)
        """,
        (sequence_name, datetime.now(timezone.utc))
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
        "UPDATE sequence_execution SET end_date = ? WHERE rowid = ?",
        (datetime.now(timezone.utc), rowid)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return rowid


def get_executions(sequence_name: str) -> list[dict]:
    connection = sqlite3.connect('file:chef.db?mode=ro', uri=True)
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT
            rowid,
            sequence_name,
            init_date,
            end_date
        FROM
            sequence_execution
        WHERE
            sequence_name = ?
        ''',
        (sequence_name,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    result_dict = []
    for row in rows:
        result_dict.append({
            'id': row[0],
            'sequence_name': row[1],
            'init_date': row[2],
            'end_date': row[3]
        })

    return result_dict


def remove_old():
    connection = sqlite3.connect('chef.db')
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM
            sequence_execution
        WHERE
            init_date = ?
        """,
        (LOG_RETENTION,)
    )
    connection.commit()
    cursor.close()
    connection.close()
