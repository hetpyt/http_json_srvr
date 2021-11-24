
from http.server import HTTPServer
from JSONRequestHandler import JSONRequestHandler
from config.config import Config

if __name__ == '__main__':
    server = HTTPServer((Config.host, Config.port), JSONRequestHandler)
    server.serve_forever()

