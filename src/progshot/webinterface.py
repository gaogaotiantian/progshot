from .cli import CLI


class WebInterface(CLI):
    def __init__(self, filename, enable_rich=False):
        super().__init__(filename, enable_rich=enable_rich)
        self.output = ""

    def get_source(self):
        code = self.viewer.get_source(self.curr_frame.filename)
        return {"code": code,
                "curr_lineno": self.curr_frame.curr_lineno,
                "locals": self.get_locals()}

    def get_locals(self):
        res = ""
        for key, val in self.curr_frame.locals.items():
            res += str(key) + " = " + str(val) + "\n"
        return res

    def get_stack(self):
        self.parse_cmd("w")
        return self.get_output()

    def get_output(self):
        return self.output

    def parse_cmd(self, cmd):
        self.output = ""
        return super().parse_cmd(cmd)

    def _show_code(self, code, start_lineno, curr_lineno=set()):
        self.output += code + "\n"

    def message(self, s):
        self.output += str(s) + "\n"

    def info(self, s):
        self.output += str(s) + "\n"

    def error(self, s):
        self.output += "Error: " + str(s) + "\n"
