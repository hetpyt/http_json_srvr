
from http.server import BaseHTTPRequestHandler
from json import dumps as json_dumps, loads as json_loads
from json.decoder import JSONDecodeError
from DataStore import DataStoreError, DataStore


class JSONRequestHandler(BaseHTTPRequestHandler):
    def response_write(self, text):
        self.wfile.write(bytes(text, encoding='utf-8'))

    def response_headers(self):
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

    def json_response(self, data):
        self.send_response(200)
        self.response_headers()
        self.response_write(json_dumps(data))

    def json_error(self, code, message=""):
        self.send_response(code)
        self.response_headers()
        self.response_write(json_dumps("FAIL"))

    def do_GET(self):
        ds = DataStore()
        data = ds.query()
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.response_write(data)

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        if length:
            try:
                data = json_loads(self.rfile.read(length))
            except JSONDecodeError:
                self.json_error(400)
                return

            # store data
            ds = DataStore()
            try:
                ds.save(data)
            except DataStoreError as e:
                print(e)
                self.json_error(500)
                return

            # return answer
            self.json_response("OK")

