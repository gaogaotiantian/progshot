import unittest
import subprocess


class TestWebInterface(unittest.TestCase):
    def setUp(self):
        subprocess.Popen(["pswebserver", "out.pshot"])