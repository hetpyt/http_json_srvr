from datetime import datetime as dt
from config.config import Config
import sqlite3


class DataStoreError(Exception):
    pass


class DataStore:
    __lock_file = False

    @classmethod
    def lock(cls):
        # waiting for unlock file
        while cls.is_lock():
            pass
        cls.__lock_file = True

    @classmethod
    def unlock(cls):
        cls.__lock_file = False

    @classmethod
    def is_lock(cls):
        return cls.__lock_file

    def __init__(self):
        self.__data_fields = ['node_id', 'temp', 'humi', 'qfe', 'dewp']
        self.__data_fields_all = ['id', 'date', 'time'] + self.__data_fields
        self.__file_name = Config.get('db_path')

    def save(self, data):
        if isinstance(data, dict):
            try:
                #self.__save_to_file(data)
                self.__save_to_db(data)
            except Exception as e:
                raise DataStoreError(e)
        else:
            raise DataStoreError('type error: not a dict')

    def query(self):
        return self.__query()

    def get_temp(self):
        return self.__query(['date', 'time', 'temp'])
        pass

    def get_humi(self):
        pass

    def get_qfe(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def __query(self, fields=None):
        self.lock()
        # do staf
        result = {}
        if fields is None:
            fields = self.__data_fields_all
        try:
            with sqlite3.connect(Config.get('db_path')) as conn:
                cursor = conn.cursor()
                data = cursor.execute("""
                    SELECT """ + ', '.join(fields) + """
                    FROM node_data""").fetchall()
                field_index = 0
                for field in fields:
                    field_data = []
                    for row in data:
                        field_data.append(row[field_index])
                    result[field] = field_data
                    field_index += 1
                return result
        finally:
            self.unlock()

    def __save_to_db(self, data):
        insdata = []
        for field in self.__data_fields:
            insdata.append(data.get(field))
        conn = sqlite3.connect(Config.get('db_path'))
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
        conn.commit()
        # insert data
        cursor.execute("""
            INSERT INTO node_data(node_id, temp, humi, qfe, dewp)
            VALUES(?, ?, ?, ?, ?)
            """, insdata)
        conn.commit()

    def __save_to_file(self, data):
        self.lock()
        try:
            with open(self.__file_name, 'a') as f:
                f.write('[%s]\n' % dt.now())
                for field in self.__data_fields:
                    f.write('%s=%s\n' % (field, data.get(field, 'null')))
        finally:
            self.unlock()
