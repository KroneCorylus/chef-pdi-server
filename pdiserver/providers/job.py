import sqlite3
from datetime import datetime, timezone


def insert_execution(job_name: str, pid: int, id_secuence_execution: int) -> int:
    connection = sqlite3.connect('chef.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO job_execution (job_name,pid,init_date, id_secuence_execution) VALUES (?,?,?,?)",
        (job_name, pid, datetime.now(timezone.utc), id_secuence_execution)
    )
    rowid = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return rowid


def update_execution_result(rowid: int, stdout: str, stderr: str, return_code: int):
    end_ts = datetime.now(timezone.utc)
    connection = sqlite3.connect('chef.db')
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE
            job_execution
        SET
            stdout=?,
            stderr=?,
            return_code=?,
            end_date=?
        WHERE
            rowid=?
        """,
                   (stdout, stderr, return_code, end_ts, rowid))
    connection.commit()
    cursor.close()
    connection.close()


def get_executions(job_name):
    conn = sqlite3.connect('chef.db')

    cursor = conn.cursor()

    cursor.execute(
        'SELECT rowid, pid, return_code, init_date, end_date, id_secuence_execution FROM job_execution WHERE job_name = ?', (job_name,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    result_dict = []
    for row in rows:
        result_dict.append({
            'id': row[0],
            'pid': row[1],
            'return_code': row[2],
            'init_date': row[3],
            'end_date': row[4],
            'id_secuence_execution': row[5]
        })

    return result_dict


def get_execution(job_name, rowid):
    conn = sqlite3.connect('chef.db')

    cursor = conn.cursor()

    cursor.execute(
        'SELECT stdout FROM job_execution WHERE job_name = ? AND rowid = ?', (job_name, rowid))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else "log no encontrado"
