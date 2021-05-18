# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import os
import progshot
import unittest
from .cli_tmpl import CLITmpl


class TestProgShot(unittest.TestCase):
    def test_capture(self):
        ps = progshot.ProgShot(save_at_exit=False)
        ps.capture()
        ps.dump("test.pshot")
        self.assertTrue(os.path.exists("test.pshot"))
        self.assertTrue(os.stat("test.pshot").st_size > 0)
        os.remove("test.pshot")

    def test_config(self):
        ps = progshot.ProgShot()
        self.assertEqual(ps._save_at_exit, True)
        ps.config(save_at_exit=False)
        self.assertEqual(ps._save_at_exit, False)
        with self.assertRaises(TypeError):
            ps.config(save_at_exit="False")


class TestProgshotCLI(CLITmpl):
    def test_gen(self):
        self.test_dir = os.path.dirname(__file__)
        for dirpath, _, files in os.walk(os.path.join(self.test_dir, "test_scripts")):
            for filename in files:
                self.generate_progshot(os.path.join(dirpath, filename))
                self.assertTrue(os.path.exists("out.pshot"))
                os.remove("out.pshot")
