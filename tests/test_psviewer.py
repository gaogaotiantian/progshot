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
        t.run()

    def test_next(self):
        t = self.create_test("out.pshot")
        t.command("n")
        t.check_in("def func_f(i)")
        t.command("p i")
        t.check_in("1")
        t.command("next")
        t.command("p i")
        t.check_in("2")
        t.command("next 2")
        t.command("p i")
        t.check_in("4")
        t.run()

    def test_back(self):
        t = self.create_test("out.pshot")
        t.command("n 5")
        t.command("b")
        t.command("p i")
        t.check_in("4")
        t.command("b 2")
        t.command("p i")
        t.check_in("2")
        t.command("back")
        t.command("p i")
        t.check_in("1")
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

    def test_goto(self):
        t = self.create_test("out.pshot")
        t.command("g 2")
        t.command("p i")
        t.check_in("1")
        t.command("goto Film-4")
        t.check_in("3")
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
        t.run()

    def test_rich(self):
        t = self.create_test("out.pshot", enable_rich=True)
        t.command("ll")
        t.check_in("func_f")
        t.run()
