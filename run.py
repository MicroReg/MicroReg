from server.Server import Server

if __name__ == '__main__':
    s = Server('localhost', 8000, 1)
    s.serve()
