from datetime import datetime as dt
from config.config import Config
import sqlite3


class DataStoreError(Exception):
    pass


class DataStore:
    def __init__(self):
        self.__data_fields = ['node_id', 'temp', 'humi', 'qfe', 'dewp']
        self.__data_fields_all = ['id', 'date', 'time'] + self.__data_fields
        self.__file_name = Config.get('db_path')
        try:
            self.__conn = sqlite3.connect(self.__file_name)
        except Exception as e:
            raise DataStoreError(e)

    def save(self, data):
        if isinstance(data, dict):
            try:
                self.__save_to_db(data)
            except Exception as e:
                raise DataStoreError(e)
        else:
            raise DataStoreError('type error: not a dict')

    def query(self):
        return self.__query()

    def get_nodes_id(self):
        pass

    def get_temp(self):
        return self.__query(['temp'])

    def get_humi(self):
        return self.__query(['date', 'time', 'humi'])

    def get_qfe(self):
        return self.__query(['date', 'time', 'qfe'])

    def get_dewp(self):
        return self.__query(['date', 'time', 'dewp'])

    def __query(self, fields=None):
        try:
            result = {}
            cursor = self.__conn.cursor()
            rows = cursor.execute("""
                SELECT node_id
                FROM node_data
                GROUP BY node_id""").fetchall()
            for row in rows:
                node_id = row[0]
                result[str(node_id)] = self.__query_node(fields, node_id)
            return result
        except Exception as e:
            raise DataStoreError(e)

    def __query_node(self, fields, node_id):
        if fields is None:
            fields = self.__data_fields_all
        try:
            cursor = self.__conn.cursor()
            data = cursor.execute("""
                SELECT date || ' ' || time, """ + ', '.join(fields) + """
                FROM node_data
                WHERE node_id = ?""", (node_id, )).fetchall()
            return QueryResult(fields, data)
        except Exception as e:
            raise DataStoreError(e)

    def __save_to_db(self, data):
        insdata = []
        for field in self.__data_fields:
            insdata.append(data.get(field))
            # TODO add node_id field to esp firmware
        # insert data
        self.__conn.cursor().execute("""
            INSERT INTO node_data(node_id, temp, humi, qfe, dewp)
            VALUES(?, ?, ?, ?, ?)
            """, insdata)
        self.__conn.commit()


class QueryResult:
    def __init__(self, fields, rows):
        self.__fields = fields
        self.__rows = rows

    def __iter__(self):
        self.__iter = self.__rows.__iter__()
        return self

    def __next__(self):
        row = self.__iter.next()
        return {self.__fields[i]: row[i] for i in range(self.__fields.count())}

    def __getattr__(self, item):
        if item == 'fields':
            return self.__fields
        elif item == 'rows':
            return self.__rows
        else:
            raise AttributeError

