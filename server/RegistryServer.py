from Server import Server
from database.ServiceDB import ServiceDB

class RegistryServer:
    '''
    Registry Server provides a running server for interacting with the ServiceDB
    '''

    def __init__(self, host='localhost', port='8800', debug=0):
        ''' Initialize the RegistryServer '''

        self.__registry_server = Server(host, port, debug)
        self.__service_db = ServiceDB()
        self.__service_reg = {}
        self.__registry_server.register_handler(self.register, "register")
        self.__registry_server.register_handler(self.update_status, "update_status")
        self.__registry_server.register_handler(self.unregister, "unregister")
        self.__registry_server.register_handler(self.get_service_details, "get_service_details")
        self.__registry_server.serve()

    def register(self, service_name, service_host, service_port, service_status=ServiceDB.SERVICE_RUNNING):
        ''' Register the service with the Database '''

        resp = self.__service_db.register_service(service_name, service_host, service_port, service_status)
        if resp != False:
            self.__service_reg[service_name] = resp
            print self.__service_reg
        return resp

    def update_status(self, service_name, service_status):
        ''' Update the service status in ServiceDB '''

        if service_name not in self.__service_reg:
            return False
        service_id = self.__service_reg[service_name]
        return self.__service_db.update_service_status(service_id, service_status)

    def get_service_details(self, service_name):
        ''' Returns the service status '''

        if service_name not in self.__service_reg:
            return False
        service_id = self.__service_reg[service_name]
        return self.__service_db.get_service_location(service_id)

    def unregister(self, service_name):
        ''' Unregister the service from the ServiceDB '''

        if service_name not in self.__service_reg:
            return False
        service_id = self.__service_reg[service_name]
        self.__service_reg[service_name]
        print self.__service_reg
        return self.__service_db.unregister_service(service_id)
