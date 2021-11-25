import math

from config.config import Config
import sqlite3
import random as r
from random import random, randint, uniform


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


if __name__ == '__main__':
    init_db()
    fill_test_data()
