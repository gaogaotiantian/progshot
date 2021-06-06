# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import inspect
import os
import progshot
from progshot.film import Film
import tempfile
import unittest
from unittest.mock import patch
from .cli_tmpl import CLITmpl


class TestProgShot(unittest.TestCase):
    def test_capture(self):
        ps = progshot.ProgShot(save_at_exit=False)
        ps.capture()
        ps.dump("test.pshot")
        self.assertTrue(os.path.exists("test.pshot"))
        self.assertTrue(os.stat("test.pshot").st_size > 0)
        os.remove("test.pshot")

    def test_capture_lambda(self):
        ps = progshot.ProgShot(save_at_exit=False)
        _ = max([1, 2, 3], key=lambda _: ps.capture() or 1)
        self.assertEqual(len(ps._films), 3)

    def test_capture_without_filename(self):
        def f(ps):
            ps.capture()
        ps = progshot.ProgShot(save_at_exit=False)
        with patch.object(inspect, "getsourcelines", return_value=None, side_effect=OSError()) as _:
            f(ps)
            film = Film(ps._films[-1])
            self.assertEqual(film.frames[0].start_lineno, -1)
            self.assertEqual(film.frames[0].frame_lines, 0)

    def test_config(self):
        ps = progshot.ProgShot()
        self.assertEqual(ps._save_at_exit, True)
        ps.config(save_at_exit=False)
        self.assertEqual(ps._save_at_exit, False)
        ps.config(save_at_exit=True)
        self.assertEqual(ps._save_at_exit, True)
        with self.assertRaises(TypeError):
            ps.config(save_at_exit="False")

        ps.config(depth=3)
        self.assertEqual(ps._trace_config["depth"], 3)
        with self.assertRaises(ValueError):
            ps.config(depth="lol")

    def test_dump(self):
        ps = progshot.ProgShot(save_at_exit=False)
        ps.capture()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pshot", delete=False) as f:
            ps.dump(f.name, clear_data=False)
        self.assertTrue(os.path.exists(f.name))
        os.remove(f.name)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".pshot", delete=False) as f:
            ps.config("filename", f.name)
            ps.dump()
        self.assertTrue(os.path.exists(f.name))
        os.remove(f.name)


class TestProgshotCLI(CLITmpl):
    def test_gen(self):
        self.test_dir = os.path.dirname(__file__)
        for dirpath, _, files in os.walk(os.path.join(self.test_dir, "test_scripts")):
            for filename in files:
                self.generate_progshot(os.path.join(dirpath, filename))
                self.assertTrue(os.path.exists("out.pshot"))
                os.remove("out.pshot")
