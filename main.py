
from http.server import HTTPServer
from JSONRequestHandler import JSONRequestHandler


if __name__ == '__main__':
    server = HTTPServer(("192.168.1.114", 80), JSONRequestHandler)
    server.serve_forever()

