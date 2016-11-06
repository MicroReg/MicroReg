from BaseHTTPServer import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    '''
    Handles the HTTP Requests arising from the Microservices
    '''

    def do_GET(self):
        ''' Handle the GET Requests originating from the client '''

        try:
            self.send_response(200)
            self.send_header('Content-Type','text/html')
            self.end_headers()
            self.wfile.write("Hello world!")
        except AttributeError:
            print "Illegal Operation Attempted"
        return

    def do_POST(self):
        ''' Handle the POST requests originating from the Microservices '''

        try:
            self.send_response(200)
            self.send_header('Content-Type','Application/JSON')
            self.end_headers()
            self.wfile.write("{'result': 'Accepted'}")
        except AttributeError:
            print "Illegal Operation Attempted"
        return
