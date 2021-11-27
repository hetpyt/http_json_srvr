
from http.server import BaseHTTPRequestHandler
from json import dumps as json_dumps, loads as json_loads
from json.decoder import JSONDecodeError
from DataStoreDB import DataStoreError, DataStore
from ChartView import ChartView


class JSONRequestHandler(BaseHTTPRequestHandler):
    def response_write(self, text):
        self.wfile.write(bytes(text, encoding='utf-8'))

    def response_headers(self, content_type='text/plain', charset='utf-8'):
        self.send_header("Content-type", "%s; charset=%s" % (content_type, charset))
        self.end_headers()

    def json_response(self, data):
        self.send_response(200)
        self.response_headers('application/json')
        self.response_write(json_dumps(data))

    def json_error(self, code, message=""):
        self.send_response(code)
        self.response_headers()
        self.response_write(json_dumps("FAIL"))

    def do_GET(self):
        path_list = self.path.strip('/').split('/')
        if len(path_list) > 0:
            if path_list[0] == 'chart':
                ds = DataStore()
                print('path=%s' % self.path)
                try:
                    view = ChartView(ds, path_list[1] if len(path_list) > 1 else '')
                except Exception as e:
                    self.json_error(404)
                self.send_response(200)
                self.response_headers('text/html')
                self.response_write(view.render())
            else:
                self.json_error(404)
        else:
            self.json_error(404)

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

