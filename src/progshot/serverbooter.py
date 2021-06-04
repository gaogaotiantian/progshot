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
from .webinterface import WebInterface


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
    def __init__(self, options):
        self.httpd = None
        self.options = options

    def start_frontend(self):
        socketserver.TCPServer.allow_reuse_address = True
        socket.setdefaulttimeout(2)
        self.httpd = socketserver.TCPServer(("", FRONTENDPORT), Handler)
        self.httpd.serve_forever()

    async def async_main(self, web_server):
        stop = asyncio.get_event_loop().create_future()
        import signal
        asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, stop.set_result, None)
        asyncio.get_event_loop().add_signal_handler(signal.SIGINT, stop.set_result, None)
        async with websockets.serve(web_server.communication, HOSTNAME, SERVERPORT):
            await stop


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
    web_interface = WebInterface(fp)
    web_server = ProgShotWebServer(web_interface)
    print("server is running at localhost:8000")
    serverboot = ServerBooter(options)
    front_end_thread = threading.Thread(target=serverboot.start_frontend, daemon=True)
    front_end_thread.start()
    asyncio.run(serverboot.async_main(web_server))
    serverboot.httpd.shutdown()
    front_end_thread.join()


if __name__ == "__main__":
    web_server_main()
