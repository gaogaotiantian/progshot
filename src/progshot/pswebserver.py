import asyncio
import websockets
import json
import sys
from .webinterface import WebInterface

hostName = "localhost"
serverPort = 8080


class ProgShotWebServer:
    def __init__(self, web_interface):
        self.web_interface = web_interface

    async def communication(self, websocket, path):
        async for message in websocket:
            request = json.loads(message)
            response = self.parse_request(request)
            await websocket.send(json.dumps(response))

    def parse_request(self, req):
        print(req)
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
            print(self.web_interface.curr_frame_idx)
            print(res)
        return res

    def exe_command(self, command):
        self.web_interface.parse_cmd(command)
        return {
            "console": self.web_interface.get_output(),
            "source": self.web_interface.get_source()
        }


def web_server_main():
    if len(sys.argv) != 2:
        print("Need one argument!", file=sys.stderr)
        exit(1)
    web_interface = WebInterface(sys.argv[1])
    web_server = ProgShotWebServer(web_interface)
    start_server = websockets.serve(web_server.communication, hostName, serverPort)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    web_server_main()
