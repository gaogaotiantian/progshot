# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


from .cli import CLI


class WebInterface(CLI):
    def __init__(self, filename, enable_rich=False):
        super().__init__(filename, enable_rich=enable_rich)
        self.output = ""

    def get_source(self):
        code = self.viewer.get_source(self.curr_frame.filename)
        return {
            "code": code,
            "curr_lineno": self.curr_frame.curr_lineno,
            "locals": self.get_locals(),
            "film": {
                "name": self.curr_film.name,
                "num_films": self.films_count,
                "curr_film_idx": self.curr_film_idx
            }
        }

    def get_locals(self):
        res = []
        for key, val in self.curr_frame.locals.items():
            res.append(f"{key} = {val}\n")
        return "".join(res)

    def get_stack(self):
        res = []
        for i in range(len(self.curr_film.frames) - 1, -1, -1):
            frame = self.curr_film.frames[i]
            info = {
                "idx": i + 1,
                "file_string": f"{frame.filename}({frame.curr_lineno}):{frame.co_name}",
                "code_string": self.viewer.get_source_line(
                    frame.filename,
                    frame.curr_lineno
                ).strip()
            }
            res.append(info)
        return {
            "stack": res,
            "curr": self.curr_frame_idx + 1
        }

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
