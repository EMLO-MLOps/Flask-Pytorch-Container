import sqlite3 as sl
from os.path import exists

def init_db():
    file_exists = exists('mydb.db')


    print(f"------ {file_exists} ------")
    if not file_exists:
        con = sl.connect('mydb.db')
        with con:
            con.execute("""
                CREATE TABLE MLINFER (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    inference TEXT,
                    saveLocation TEXT,
                    confidence DECIMAL
                );
            """)
    else:
        con = sl.connect('mydb.db')


def insert(output):
    sql = 'INSERT INTO MLINFER (filename, inference, saveLocation, confidence) values(?, ?, ?, ?)'
    data = [(output['filename'],
            output['inference'],
            output['confidence'],
            output['saveLocation'])]
    con = sl.connect('mydb.db')
    with con:
        con.executemany(sql, data)

    con.close()


def get_prev():
    con = sl.connect('mydb.db')
    sql = 'SELECT * FROM MLINFER LIMIT 5'
    data = con.execute(sql)
    con.close()
    return(data)
