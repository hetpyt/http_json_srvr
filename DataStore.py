from datetime import datetime as dt
from config.config import Config

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
        self.__data_fields = ['temp', 'humi', 'qfe', 'dewp']
        self.__file_name = Config.db_path

    def save(self, data):
        if isinstance(data, dict):
            try:
                self.__save_to_file(data)
            except Exception as e:
                raise DataStoreError(e)
        else:
            raise DataStoreError('type error: not a dict')

    def query(self):
        return self.__query()

    def open(self):
        pass

    def close(self):
        pass

    def __query(self):
        self.lock()
        # do staf
        try:
            with open(self.__file_name, 'r') as f:
                return f.read()
        finally:
            self.unlock()

    def __save_to_file(self, data):
        self.lock()
        try:
            with open(self.__file_name, 'a') as f:
                f.write('[%s]\n' % dt.now())
                for field in self.__data_fields:
                    f.write('%s=%s\n' % (field, data.get(field, 'null')))
        finally:
            self.unlock()
