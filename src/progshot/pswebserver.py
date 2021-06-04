import argparse
import asyncio
import http.server
import json
import os
import socketserver
import sys
import threading
import webbrowser
import websockets
from .webinterface import WebInterface

HOSTNAME = "localhost"
SERVERPORT = 8080
FRONTENDPORT = 8000
DIRECTORY = os.path.join(os.path.dirname(__file__), "frontend")


class ProgShotWebServer:
    def __init__(self, web_interface):
        self.web_interface = web_interface

    async def communication(self, websocket, path):
        async for message in websocket:
            request = json.loads(message)
            response = self.parse_request(request)
            await websocket.send(json.dumps(response))

    def parse_request(self, req):
        res = {}
        if req["type"] == "init":
            res = {
                "source": self.web_interface.get_source(),
                "stack": self.web_interface.get_stack()
            }
        elif req["type"] == "console":
            self.web_interface.parse_cmd(req["command"])
            res = {
                "console": self.web_interface.get_output(),
                "source": self.web_interface.get_source(),
                "stack": self.web_interface.get_stack()
            }
        elif req["type"] == "command":
            self.web_interface.parse_cmd(req["command"])
            res = {
                "source": self.web_interface.get_source(),
                "stack": self.web_interface.get_stack()
            }
        return res


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass


async def async_main(web_server):
    stop = asyncio.get_event_loop().create_future()
    import signal
    asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, stop.set_result, None)
    asyncio.get_event_loop().add_signal_handler(signal.SIGINT, stop.set_result, None)
    async with websockets.serve(web_server.communication, HOSTNAME, SERVERPORT):
        await stop


def start_frontend():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", FRONTENDPORT), Handler) as httpd:
        httpd.serve_forever()


def web_server_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs=1, help="pshot file to open")
    parser.add_argument("--server_only", "-s", default=False, action="store_true",
                        help="Only start the server, do not open webpage")
    options = parser.parse_args(sys.argv[1:])
    f = options.file[0]
    frontEnd = threading.Thread(target=start_frontend, daemon=True)
    frontEnd.start()
    if not options.server_only:
        webbrowser.open_new_tab(f'http://127.0.0.1:{FRONTENDPORT}')
    web_interface = WebInterface(f)
    web_server = ProgShotWebServer(web_interface)
    print("server is running at localhost:8000")
    asyncio.run(async_main(web_server))


if __name__ == "__main__":
    web_server_main()
