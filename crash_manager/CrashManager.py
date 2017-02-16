import json
import os
import time

class CrashManager:
    '''
    CrashManager periodically backups the data stored in the ServiceDB to a
    secondary storage. In case of a crash, the ServiceDB is repopulated on the
    next run from the backed up data.
    '''

    def __init__(self, service_db, backup_dir, registry_server):
        '''
        Initialize the CrashManager
        Keyword arguments:
        service_db -- The service database object from which backup happens
        backup_dir -- The path to the backup directory
        registry_server -- The registry_server instance
        '''

        self.__service_db = service_db  #Store a copy of ServiceDB object
        self.__backup_location = os.path.join(backup_dir, 'servicedb_backup.db')
        self.__backup_file_handle = open(self.__backup_location, 'r+')
        self.__registry_server = registry_server
        self.restore_data()
        self.__backup_file_handle.close()


    def __prepare_backup(self, data, safe=False):
        '''
        Prepare the backup to be written to the storage
        Keyword arguments:
        data -- The data to be backed up
        safe -- Whether the data was saved due to crash or normal shutdown (Default: False)
        Returns a dictionary containing backup data
        '''

        service_data = json.loads(data)     #Load the service data as dictionary
        backup_data = {
            'service_data': service_data
        }

        if safe == False:
            backup_data['crash_occured'] = True,
        else:
            backup_data['crash_occured'] = False

        return backup_data

    def backup_data(self, auto=True):
        '''
        Backups the data to the storage
        Keyword arguments:
        auto -- Whether the call was automatic or explicitly invoked (default: True)
        '''

        while True:
            if auto == False:
                safe = True
            else:
                safe = False
            service_data = self.__service_db.get_services()
            backup_data = self.__prepare_backup(service_data, safe)
            with open(self.__backup_location, "rw+") as backup_file:
                json.dump(backup_data, backup_file)
            time.sleep(5)

    def restore_data(self):
        '''
        Restore the data into ServiceDB from the storage
        '''

        try:
            temp_data = self.__backup_file_handle.read()
            backup_data = json.loads(temp_data)
            for service_key, service_value in backup_data['service_data'].iteritems():
                self.__registry_server.register(service_value['name'], service_value['host'], service_value['port'], service_value['status'])
        except KeyError:
            print "no key"
        except:
            print "no backup data"
