# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import json
from .webinterface import WebInterface


class ProgShotWebServer:
    def __init__(self, filepath):
        self.web_interface = WebInterface(filepath)

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
