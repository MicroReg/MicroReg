from BaseHTTPServer import HTTPServer
from RequestHandler import Handler

class Server:
    '''
    Provide HTTP Server Interface for the Application
    '''

    def __init__(self, host='localhost', port='8800', debug=0):
        ''' Instantiate the Server '''

        self.host = host
        self.port = port
        self.debug = debug

    def serve(self):
        ''' Start serving requests '''

        try:
            self.server = HTTPServer((self.host, self.port), Handler)
            if self.debug:
                print "Started Registry Server at %s:%d" %(self.host, self.port)
            self.server.serve_forever()
        except AttributeError:
            if self.debug:
                print "Illegal Operation"
        except KeyboardInterrupt:
            self.close()

    def close(self):
        ''' Stop Serving Requests '''

        if self.server:
            if self.debug:
                print "Registry Server Stopped"
            self.server.socket.close()
            return 0
        else:
            return -1
