
from http.server import HTTPServer
from JSONRequestHandler import JSONRequestHandler


if __name__ == '__main__':
    server = HTTPServer(("localhost", 80), JSONRequestHandler)
    server.serve_forever()

