import argparse
import asyncio
import functools
import http.server
import os
from objprint import objprint
import signal
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
    def __init__(self, options, web_server):
        self.httpd = None
        self.options = options
        self.stop = None
        self.web_server = web_server
        self.ws_server = None

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
    if not options.server_only:
        import webbrowser
        webbrowser.open_new_tab(f'http://{HOSTNAME}:{FRONTENDPORT}')
    fp = options.file[0]
    filename = os.path.basename(fp)
    if not filename.endswith("pshot"):
        print(f"Do not support file type {filename}")
        exit(1)
    web_server = ProgShotWebServer(fp)
    print("server is running at localhost:8000")
    serverboot = ServerBooter(options, web_server)
    serverboot.run()


if __name__ == "__main__":
    web_server_main()
