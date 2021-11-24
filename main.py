
from http.server import HTTPServer
from JSONRequestHandler import JSONRequestHandler
from config.config import Config

if __name__ == '__main__':
    server = HTTPServer((Config.get('host'), Config.get('port')), JSONRequestHandler)
    server.serve_forever()

