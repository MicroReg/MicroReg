import json

class MicroDB:
    '''
    MicroDB is an in-memory database, exposing a JSON based API to manage and work
    with the database.
    The implementation is useful for managing small sets of data inside the memory
    without additional overhead of maintaining database files on the drive.
    '''

    def __init__(self):
        ''' Instantiate the Database Object '''

        self.__db = {}  #Object parameters
        self.__num_records = 0
        self.__records = {}

    def insert(self, key, value):
        ''' Insert a new value into the record '''

        if key not in self.__records:
            self.__records[key] = value
            self.__num_records += 1
            return True

        return self.update(key,value)

    def update(self, key, value):
        ''' Update a previous value present in the database '''

        if key not in self.__records:
            return False
        self.__records[key] = value
        return True

    def get(self, key):
        ''' Get the value from the database record, with the provided key '''

        if key not in self.__records:
            raise KeyError("Provided key is not in the database")
            return
        return self.__records[key]

    def remove(self, key):
        ''' Remove a value pertaining to the key '''

        if key not in self.__records:
            raise KeyError("Provided key is not in the database")
            return
        del self.__records[key]
        self.__num_records-=1
        return True

    def get_records_json(self):
        ''' Return the records stored as a JSON data '''

        return json.dumps(self.__records)

    def get_record_count(self):
        ''' Return the total number of records stored in the database '''

        return self.__num_records
