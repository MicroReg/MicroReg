from Server import Server
from database.ServiceDB import ServiceDB
import socket
import threading
import time

class RegistryServer:
    '''
    Registry Server provides a running server for interacting with the ServiceDB
    '''

    def __init__(self, host='localhost', port='8800', debug=0):
        ''' Initialize the RegistryServer '''

        self.__registry_server = Server(host, port, debug)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__service_db = ServiceDB()
        self.__service_reg = {}
        self.__registry_server.register_handler(self.register, "register")
        self.__registry_server.register_handler(self.update_status, "update_status")
        self.__registry_server.register_handler(self.unregister, "unregister")
        self.__registry_server.register_handler(self.get_all_service_details, "get_all_service_details")
        self.__registry_server.register_handler(self.get_service_details, "get_service_details")
        self.__registry_server.register_handler(self.get_reg_count, "get_reg_count")
        self.__cron_thread = threading.Thread(target=self.service_cron, args=(self,))
        self.__cron_thread.daemon = True
        self.__cron_thread.start()
        self.__registry_server.serve()

    def service_cron(self, instance):
        '''
        Run a routine job to scan the registered service status and update it
        whenever a change is detected.
        '''

        while True:
            print instance.get_all_service_details()
            try:
                service_reg = instance.__service_reg.copy()
                for key in service_reg:
                    service = instance.get_service_details(key)
                    service_id = instance.__service_reg[key]
                    if instance.__service_db.get_service_status(service_id) == ServiceDB.SERVICE_ERROR:
                        instance.unregister(key)
                    __socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        __socket.connect((service[0].replace('http://', ''), service[1]))
                        __socket.shutdown()
                        __socket.close()
                    except socket.error as e:
                        instance.update_status(key, ServiceDB.SERVICE_ERROR)
                    except TypeError:
                        pass
            except:
                pass
            time.sleep(5)

    def register(self, service_name, service_host, service_port, service_status=ServiceDB.SERVICE_RUNNING):
        ''' Register the service with the Database '''

        if service_name in self.__service_reg:
            return False
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

    def get_all_service_details(self):
        '''Returns the complete data of all the services'''

        print "Service details call"
        return self.__service_db.get_services()

    def get_reg_count(self):
        '''Return the number of registered services'''

        return self.__service_db.get_registration_count()

    def unregister(self, service_name):
        ''' Unregister the service from the ServiceDB '''

        if service_name not in self.__service_reg:
            return False
        service_id = self.__service_reg[service_name]
        del self.__service_reg[service_name]
        print self.__service_reg
        return self.__service_db.unregister_service(service_id)
