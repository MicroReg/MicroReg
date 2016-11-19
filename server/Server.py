import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

class Server:
    '''
    Provide an XMLRPC Server for the Service Registry to allow the interacting
    Microservices to make remote procedure calls to the service database.
    '''

    def __init__(self, host='localhost', port='8800', debug=0):
        ''' Instantiate the Server '''

        self.host = host
        self.port = port
        self.debug = debug
        self.__server = SimpleXMLRPCServer((self.host, self.port))

    def serve(self):
        ''' Start serving requests '''

        try:
            if self.debug:
                print "Started Registry Server at %s:%d" %(self.host, self.port)
            self.__server.serve_forever()
        except AttributeError:
            if self.debug:
                print "Illegal Operation"
        except KeyboardInterrupt:
            self.close()

    def close(self):
        ''' Stop Serving Requests '''

        if self.__server:
            if self.debug:
                print "Registry Server Stopped"
            self.__server.server_close()
            return 0
        else:
            return -1

    def register_handler(self, func, name):
        ''' Register a new handler with the server '''

        if self.__server:
            self.__server.register_function(func, name)
            return True
        return False
