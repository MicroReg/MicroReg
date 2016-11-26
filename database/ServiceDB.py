from MicroDB import MicroDB
import datetime
import json

class ServiceDB:
    '''
    ServiceDB is an in-memory database to store the information about running
    Microservices.
    The Implementation is based upon MicroDB and provides sets of APIs through
    which the service registry is stored inside the database
    '''

    #Service status constants
    SERVICE_RUNNING = 1
    SERVICE_STOPPED = 0
    SERVICE_ERROR = -1

    def __init__(self):
        ''' Initialize the ServiceDB '''

        self.__db = MicroDB()
        self.__num_registered_services = 0
        self.__service_id_reg = 1 #Assign an auto incrementing ID to services

    def register_service(self, service_name, service_host, service_port, service_status=SERVICE_RUNNING):
        ''' Register a new service into the ServiceDB '''

        service = {}
        service['name'] = service_name
        service['host'] = service_host
        service['port'] = service_port
        service['status'] = service_status
        service['reg_timestamp'] = datetime.datetime.now()
        service['id'] = self.__service_id_reg

        #Insert into the database
        status = self.__db.insert(service['id'], service)
        if status == True:
            self.__num_registered_services += 1
            self.__service_id_reg += 1
            return service['id']
        return False

    def update_service_status(self, service_id, service_status):
        ''' Update the status of a service in ServiceDB '''

        try:
            service = self.__db.get(service_id)
            service['status'] = service_status
            return self.__db.update(service_id, service)
        except KeyError:
            return False

    def get_service_status(self, service_id):
        ''' Return the current status of the service '''

        try:
            service = self.__db.get(service_id)
            return service['status']
        except KeyError:
            return False

    def get_service_location(self, service_id):
        ''' Get the location information of a particular service '''

        try:
            service = self.__db.get(service_id)
            return (service['host'], service['port'])
        except KeyError:
            return False

    def unregister_service(self, service_id):
        ''' Unregister a service from the ServiceDB '''

        try:
            self.__db.remove(service_id)
            print "Service unregistered"
            self.__num_registered_services -= 1
            return True
        except KeyError:
            return False

    def get_services(self):
        ''' Get information about all the registered services '''

        return self.__db.get_records_json()

    def get_registration_count(self):
        ''' Get the number of services registered in the ServiceDB '''

        return self.__num_registered_services
