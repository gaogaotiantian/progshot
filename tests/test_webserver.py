# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import asyncio
import json
import os
import signal
import subprocess
import sys
import time
import unittest
import websockets


class TestWebInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cmd = ["python", os.path.join(os.path.dirname(__file__), "test_scripts", "basic.py")]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=30)
        cls().assertEqual(result.returncode, 0)

    def setUp(self):
        coverage = os.getenv("COVERAGE_RUN")
        if coverage:
            cmd = ["coverage", "run", "--parallel-mode", "--pylib", "-m", "progshot.serverbooter",
                   "--server_only", "out.pshot"]
        else:
            cmd = ["psview", "--server_only", "out.pshot"]
        self.server = subprocess.Popen(cmd)
        message = {"type": "init"}
        for i in range(20):
            try:
                asyncio.get_event_loop().run_until_complete(self.send_command(message))
                break
            except Exception:
                if i == 19:
                    self.tearDown()
                    raise
                time.sleep(0.5)

    def tearDown(self):
        # Wait until server finishes ws
        time.sleep(0.5)
        if sys.platform == "win32":
            self.server.terminate()
        else:
            self.server.send_signal(signal.SIGINT)
        try:
            self.server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.server.kill()
            self.server.wait(timeout=5)

    async def send_command(self, message):
        uri = "ws://localhost:8080"
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(message))
            res = await websocket.recv()
            return res

    def check_source(self, message):
        self.assertIn("source", message.keys())
        self.assertIn("code", message["source"])
        self.assertIn("curr_lineno", message["source"])
        self.assertIn("locals", message["source"])
        self.assertIn("film", message["source"])
        self.assertIn("name", message["source"]["film"])
        self.assertIn("num_films", message["source"]["film"])
        self.assertIn("curr_film_idx", message["source"]["film"])

    def check_stack(self, message):
        self.assertIn("stack", message.keys())
        self.assertIn("stack", message["stack"])
        self.assertIn("curr", message["stack"])

    def test_init(self):
        message = {"type": "init"}
        res = asyncio.get_event_loop().run_until_complete(self.send_command(message))
        res = json.loads(res)
        self.check_source(res)
        self.assertIn("i = 0", res["source"]["locals"])
        self.check_stack(res)
        self.assertEqual(len(res["stack"]["stack"]), 3)
        self.assertNotIn("console", res.keys())

    def test_command(self):
        message = {"type": "command",
                   "command": "next"}
        res = asyncio.get_event_loop().run_until_complete(self.send_command(message))
        res = json.loads(res)
        self.check_source(res)
        self.assertIn("i = 1", res["source"]["locals"])
        self.check_stack(res)
        self.assertEqual(len(res["stack"]["stack"]), 3)
        self.assertNotIn("console", res.keys())

    def test_console(self):
        message = {"type": "console",
                   "command": "where"}
        res = asyncio.get_event_loop().run_until_complete(self.send_command(message))
        res = json.loads(res)
        self.check_source(res)
        self.assertIn("i = 0", res["source"]["locals"])
        self.check_stack(res)
        self.assertEqual(len(res["stack"]["stack"]), 3)
        self.assertIn("console", res.keys())
        self.assertIn("func_f(i)\n* ", res["console"])

    def test_error(self):
        message = {"type": "console",
                   "command": "step 11"}
        res = asyncio.get_event_loop().run_until_complete(self.send_command(message))
        res = json.loads(res)
        self.check_source(res)
        self.assertIn("i = 0", res["source"]["locals"])
        self.check_stack(res)
        self.assertEqual(len(res["stack"]["stack"]), 3)
        self.assertIn("console", res.keys())
        self.assertIn("Target film is out of range", res["console"])


class TestWebServer(unittest.TestCase):
    def test_nofile(self):
        coverage = os.getenv("COVERAGE_RUN")
        if coverage:
            cmd = ["coverage", "run", "--parallel-mode", "--pylib", "-m", "progshot.serverbooter",
                   "--server_only", "nonexistfile"]
        else:
            cmd = ["psview", "--server_only", "nonexistfile"]
        code, output = subprocess.getstatusoutput(" ".join(cmd))
        self.assertEqual("File nonexistfile not found", output)
        self.assertEqual(1, code)


if __name__ == "__main__":
    unittest.main()
