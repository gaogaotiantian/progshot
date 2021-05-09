import http.server
import urllib.parse
import json
import sys
from functools import partial
from .webinterface import WebInterface

hostName = "localhost"
serverPort = 8080


class ProgShotWebServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, filename, request, client_address, server):
        self.web_interface = WebInterface(filename)
        super().__init__(request, client_address, server)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        print(parsed.path)
        if parsed.path == "/":
            source = self.web_interface.get_source()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(source), "utf-8"))
        elif parsed.path == "/command":
            self.send_response(200)
            self.end_headers()
            queries = dict(urllib.parse.parse_qsl(parsed.query))
            self.web_interface.parse_cmd(queries["command"])
            exeResult = {"console": self.web_interface.output,
                         "source": self.web_interface.get_source()}
            self.wfile.write(bytes(json.dumps(exeResult), "utf-8"))
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Hello World!", "utf-8"))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)


def web_server_main():
    if len(sys.argv) != 2:
        print("Need one argument!", file=sys.stderr)
        exit(1)
    handler = partial(ProgShotWebServer, sys.argv[1])
    webServer = http.server.HTTPServer((hostName, serverPort), handler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    web_server_main()
