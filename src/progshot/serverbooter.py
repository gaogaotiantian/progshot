# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import argparse
import asyncio
import http.server
import os
import socket
import socketserver
import sys
import threading
import websockets
from .pswebserver import ProgShotWebServer


HOSTNAME = "localhost"
SERVERPORT = 8080
FRONTENDPORT = 8000
DIRECTORY = os.path.join(os.path.dirname(__file__), "frontend")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass


class ServerBooter:
    def __init__(self, web_server, server_only=False):
        self.httpd = None
        self.server_only = server_only
        self.web_server = web_server

    def start_frontend(self):
        socketserver.TCPServer.allow_reuse_address = True
        socket.setdefaulttimeout(2)
        self.httpd = socketserver.TCPServer(("", FRONTENDPORT), Handler)
        self.httpd.serve_forever()

    async def async_main(self):
        async with websockets.serve(self.web_server.communication, HOSTNAME, SERVERPORT):
            await asyncio.Future()

    def run(self):
        self.front_end_thread = threading.Thread(target=self.start_frontend, daemon=True)
        self.front_end_thread.start()
        if not self.server_only:
            import webbrowser
            webbrowser.open_new_tab(f'http://{HOSTNAME}:{FRONTENDPORT}')
        try:
            asyncio.run(self.async_main())
        except KeyboardInterrupt:
            pass
        self.httpd.shutdown()
        self.front_end_thread.join()


def web_server_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs=1, help="pshot file to open")
    parser.add_argument("--server_only", "-s", default=False, action="store_true",
                        help="Only start the server, do not open webpage")
    options = parser.parse_args(sys.argv[1:])
    fp = options.file[0]
    if not os.path.isfile(fp):
        print(f"File {fp} not found")
        exit(1)
    web_server = ProgShotWebServer(fp)
    print(f"server is running at {HOSTNAME}:{FRONTENDPORT}")
    serverboot = ServerBooter(web_server, server_only=options.server_only)
    serverboot.run()


if __name__ == "__main__":
    web_server_main()
