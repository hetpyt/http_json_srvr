import re
import sys
from config.config import Config
import sqlite3
from random import randint, uniform


def init_db():
    with sqlite3.connect(Config.get('db_path')) as conn:
        cursor = conn.cursor()
        # create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS node_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                date TEXT DEFAULT CURRENT_DATE,
                time TEXT DEFAULT CURRENT_TIME, 
                node_id NUM,
                temp FLOAT(15, 2), 
                humi FLOAT(15, 2), 
                qfe FLOAT(15, 2), 
                dewp FLOAT(15, 2)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS _node_id ON node_data (node_id)")
        conn.commit()


def fill_test_data():
    data = []
    for i in range(20):
        node = randint(1, 2)
        if node == 1:
            row = (node, uniform(22.0, 26.0), uniform(25.0, 35.0), uniform(850.0, 1100.0), uniform(5.0, 7.0))
        else:
            row = (node, uniform(10.0, 15.0), uniform(50.0, 60.0), uniform(850.0, 1100.0), uniform(2.0, 4.0))
        data.append(row)
        print(row)
    with sqlite3.connect(Config.get('db_path')) as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO node_data(node_id, temp, humi, qfe, dewp)
            VALUES(?, ?, ?, ?, ?)
            """, data)


def load_data(file):
    """load data from text file of previous version"""
    with open(file, 'r') as f:
        lines = f.readlines()

    node = 1
    date = None
    time = None
    data = []
    row = {}
    for line in lines:
        # [2021-11-25 00:08:59.205090]
        m = re.match(r'^\[(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\.\d+\]', line)
        if m:
            print('%s -- %s' % (m[1], m[2]))
            if date:
                # add row to data
                print(row)
                data.append((date, time, node, row['temp'], row['humi'], row['qfe'], row['dewp']))
            # define new date & time
            date = m[1]
            time = m[2]
            # reset row
            row = {}
        # temp=12.34
        m = re.match(r'^(\w+)=(\d+\.*\d+)', line)
        if m:
            print('%s = %s' % (m[1], m[2]))
            row[m[1]] = float(m[2])
    data.append((date, time, node, row['temp'], row['humi'], row['qfe'], row['dewp']))

    with sqlite3.connect(Config.get('db_path')) as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO node_data(date, time, node_id, temp, humi, qfe, dewp)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """, data)


if __name__ == '__main__':
    init_db()
    if len(sys.argv) > 1:
        file_to_load = sys.argv[1]
        load_data(file_to_load)
