import sys
import sqlite3


def fetchall(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        data = cursor.execute("""
            SELECT * FROM node_data
            """)
        for row in data:
            print(row)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
        fetchall(db_path)
