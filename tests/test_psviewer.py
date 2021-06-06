# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


from .cli_tmpl import CLITmpl
import os


class TestPSVIewerBasic(CLITmpl):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(__file__)
        cls().generate_progshot(os.path.join(cls.test_dir, "test_scripts", "basic.py"), coverage=False)

    @classmethod
    def tearDownClass(cls):
        os.remove("out.pshot")

    def test_read(self):
        t = self.create_test("out.pshot")
        t.check_in("def func_f(i)")
        t.command("q")
        t.run()

    def test_list(self):
        t = self.create_test()
        t.command("l")
        t.check_in("func_f")
        t.run()

    def test_step(self):
        t = self.create_test("out.pshot")
        t.command("s")
        t.check_in("def func_f(i)")
        t.command("p i")
        t.check_in("1")
        t.command("step")
        t.command("p i")
        t.check_in("2")
        t.command("step 2")
        t.command("p i")
        t.check_in("4")
        t.run()

    def test_nextback(self):
        t = self.create_test("out.pshot")
        for _ in range(5):
            t.command("n")
        t.command("b")
        t.command("p i")
        t.check_in("4")
        t.command("back")
        t.command("p i")
        t.check_in("3")
        t.run()

    def test_up(self):
        t = self.create_test("out.pshot")
        t.command("u")
        t.check_in("func_f(i)")
        t.command("p a")
        t.check_not_in("3")
        t.run()

    def test_down(self):
        t = self.create_test("out.pshot")
        t.command("u")
        t.command("p a")
        t.check_not_in("3")
        t.command("d")
        t.command("p a")
        t.check_in("3")
        t.run()

    def test_frame(self):
        t = self.create_test("out.pshot")
        t.command("frame 3")
        t.check_in("for i")
        t.check_in("func_g")
        t.command("p i")
        t.check_in("0")
        t.command("p a")
        t.check_in("NameError")
        t.command("frame 1")
        t.command("p b")
        t.check_in("c")
        t.command("frame 100")
        t.check_in("out of")
        t.run()

    def test_goto(self):
        t = self.create_test("out.pshot")
        t.command("g 2")
        t.command("p i")
        t.check_in("1")
        t.command("goto Film-4")
        t.check_in("3")
        t.command("g")
        t.check_in("Usage")
        t.run()

    def test_where(self):
        t = self.create_test("out.pshot")
        t.command("w")
        t.check_true(lambda s: "*" in s.strip().split('\n')[-2])
        t.check_true(lambda s: "func_f" in s.strip().split('\n')[-2])
        t.command("u 10")
        t.command("w")
        t.check_true(lambda s: "*" in [line for line in s.strip().split('\n') if ":" in line][0])
        t.run()

    def test_print(self):
        t = self.create_test("out.pshot")
        t.command("p d")
        t.check_in("NameError")
        t.command("p")
        t.check_in("Usage")
        t.run()

    def test_rich(self):
        t = self.create_test("out.pshot", enable_rich=True)
        t.command("ll")
        t.check_in("func_f")
        t.command("w")
        t.check_in("basic.py")
        t.run()

    def test_invalid(self):
        t = self.create_test("out.pshot")
        t.command("invalid test")
        t.check_in("invalid test")
        t.run()

    def test_cmdline(self):
        p = self.run_cmd(["psview-cli", "out.pshot"])
        out, _ = p.communicate("q\n", timeout=5)
        self.assertIn("Film-1", out)
        p = self.run_cmd(["psview-cli", "no_such_file"])
        out, _ = p.communicate(timeout=5)
        self.assertIn("Traceback", out)


class TestPSViewerTrace(CLITmpl):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(__file__)
        cls().generate_progshot(os.path.join(cls.test_dir, "test_scripts", "trace_basic.py"), coverage=False)

    @classmethod
    def tearDownClass(cls):
        os.remove("out.pshot")

    def test_load(self):
        t = self.create_test("out.pshot")
        t.command("p i")
        t.check_in("0")
        t.command("ll")
        t.check_in("@trace")
        t.run()

    def test_where(self):
        t = self.create_test("out.pshot")
        t.command("w")
        t.check_equal(lambda s: s.count('>'), 1)
        t.run()

    def test_step(self):
        t = self.create_test("out.pshot")
        t.command("s")
        t.command("s")
        t.command("ll")
        t.check_in("random")
        t.run()

    def test_stepback(self):
        t = self.create_test("out.pshot")
        t.command("n")
        t.command("n")
        t.command("sb")
        t.command("p i")
        t.check_in("0")
        t.command("ll")
        t.check_in("random")
        for _ in range(4):
            t.command("sb")
            t.command("ll")
            t.check_in("random")
        t.command("sb")
        t.command("ll")
        t.check_not_in("random")
        t.run()

    def test_return(self):
        t = self.create_test("out.pshot")
        t.command("s")
        t.command("s")
        t.command("r")
        t.command("ll")
        t.check_not_in("random")
        t.command("p i")
        t.check_in("0")
        t.command("n")
        t.command("p _")
        t.check_in("1")
        t.run()

    def test_returnback(self):
        t = self.create_test("out.pshot")
        t.command("s")
        t.command("s")
        t.command("rb")
        t.command("ll")
        t.check_not_in("random")
        t.command("p i")
        t.check_in("0")
        t.command("n")
        t.command("p _")
        t.check_in("0")
        t.run()

    def test_until(self):
        t = self.create_test("out.pshot")
        t.command("s")
        t.command("s")
        t.command("unt")
        t.command("p a")
        t.check_in("3")
        t.command("unt 9")
        t.command("p b")
        t.check_in("c")
        t.command("unt 100")
        t.command("ll")
        t.check_in("func_g")
        t.run()

    def test_untilback(self):
        t = self.create_test("out.pshot")
        t.command("s")
        t.command("s")
        t.command("unt 9")
        t.command("untb")
        t.command("untb")
        t.command("p c")
        t.check_in("NameError")
        t.command("untb 6")
        t.command("p b")
        t.check_in("NameError")
        t.command("untb 1")
        t.command("ll")
        t.check_in("func_g")
        t.run()


class TestPSViewerInvalid(CLITmpl):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(__file__)
        cls().generate_progshot(os.path.join(cls.test_dir, "test_scripts", "trace_basic.py"), coverage=False)

    @classmethod
    def tearDownClass(cls):
        os.remove("out.pshot")

    def test_film_out_of_range(self):
        t = self.create_test()
        t.command("b")
        t.check_in("out of range")
        t.command("rb")
        t.check_in("out of range")
        t.command("sb")
        t.check_in("out of range")
        t.command("untb")
        t.check_in("out of range")
        t.command(["d" for _ in range(5)])
        t.check_in("newest")
        t.command("g -1")
        t.command("n")
        t.check_in("out of range")
        t.command("r")
        t.check_in("out of range")
        t.command("s")
        t.check_in("out of range")
        t.command("unt")
        t.check_in("out of range")
        t.command("g 1000")
        t.check_in("out of range")
        t.command("g invalid")
        t.check_in("Error")
        t.run()

    def test_invalid_args(self):
        t = self.create_test()
        t.command("w 1")
        t.check_in("Error")
        t.command("d 15 15")
        t.check_in("Error")
        t.command("d lol")
        t.check_in("Error")
        t.command("invalid lol")
        t.check_in("Unknown")
        t.command("")
        t.check_true(lambda s: len(s) < 3)
        t.run()


class TestPSViewerClass(CLITmpl):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(__file__)
        cls().generate_progshot(os.path.join(cls.test_dir, "test_scripts", "trace_class.py"), coverage=False)

    @classmethod
    def tearDownClass(cls):
        os.remove("out.pshot")

    def test_pprint(self):
        t = self.create_test("out.pshot")
        t.command("n")
        t.command("pp a")
        t.check_in(["Data", "a", "b", "c"])
        t.command("pp")
        t.check_in("Usage")
        t.command("pp d")
        t.check_in("NameError")
        t.run()
