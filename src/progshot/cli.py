# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import argparse
import functools
from rich.console import Console
from rich.syntax import Syntax
import sys
import traceback
from .psviewer import ProgShotViewer
try:
    import readline
    # remove some common file name delimiters
    readline.set_completer_delims(' \t\n`@#$%^&*()=+[{]}\\|;:\'",<>?')
except ImportError:
    pass


def check_args(arg_types, default):
    if not isinstance(arg_types, tuple) and arg_types is not None:
        arg_types = (arg_types, )
    if not isinstance(default, tuple):
        default = (default, )

    def decorator_check(func):
        @functools.wraps(func)
        def wrapper(self, args):
            parsed_args = []
            if arg_types is None:
                if len(args) > 0:
                    self.error(f"Unexpected arguments {' '.join(args)}")
                    return
            else:
                if len(args) > len(arg_types):
                    self.error(f"Unexpected arguments {' '.join(args)}")
                    return
                for idx, t in enumerate(arg_types):
                    if idx < len(args):
                        try:
                            parsed_args.append(t(args[idx]))
                        except ValueError:
                            self.error(f"Invalid argument {args[idx]}")
                            return
                    else:
                        if idx < len(default):
                            parsed_args.append(default[idx])
                        else:
                            self.error("Missing argument")
                            return

            return func(self, *parsed_args)
        return wrapper
    return decorator_check


class CLI:
    def __init__(self, filename, enable_rich=True):
        self.filename = filename
        self.viewer = ProgShotViewer(filename)
        self.enable_rich = enable_rich
        self.console = Console()
        self._switch_film(0)

    def run(self):
        self._show_curr_frame()
        while True:
            try:
                cmd = input(">>> ")
                if self.parse_cmd(cmd):
                    break
            except EOFError:
                break

    def parse_cmd(self, cmd):
        """
        retval: whether to exit the cli
        """
        args = cmd.split()

        if not args:
            return False

        cmd = args[0]
        cmd_args = args[1:]

        try:
            func = getattr(self, "do_" + cmd)
        except AttributeError:
            return self._do_default(cmd)
        finish = func(cmd_args)
        if finish is None:
            return False
        else:
            return finish

    def _switch_film(self, film_idx):
        if 0 <= film_idx < len(self.viewer.films):
            self.curr_film_idx = film_idx
            self.curr_film = self.viewer.films[film_idx]
            self.curr_frame_idx = 0
            self.curr_frame = self.curr_film.frames[self.curr_frame_idx]
            return True
        return False

    def _show_curr_frame(self, lineno=None):
        if lineno is None:
            lineno = self.curr_frame.curr_lineno
        start = lineno - 5
        end = lineno + 6
        code = self.viewer.get_source_lines(
            self.curr_frame.filename,
            start,
            end
        )
        self._show_code(code, start, curr_lineno=self.curr_frame.curr_lineno)

    def _show_code(self, code, start_lineno, curr_lineno=set()):
        highlight_lines = {curr_lineno}
        if self.enable_rich:
            syntax = Syntax(code, "python", line_numbers=True, start_line=start_lineno, highlight_lines=highlight_lines)
            self.console.print(syntax)
        else:
            self.message(code)

    def error(self, s):
        print(f"Error, {s}")

    def info(self, s, end="\n"):
        print(s, end=end)

    def message(self, s):
        if self.enable_rich:
            self.console.print(s)
        else:
            print(s)

    def _do_default(self, args):
        print(f"unknown syntax {args}")
        return False

    def _get_val(self, val):
        return eval(val, {}, self.curr_frame.locals)

    def do_longlist(self, args):
        curr_frame = self.curr_frame
        code = self.viewer.get_source_lines(
            curr_frame.filename,
            curr_frame.start_lineno,
            curr_frame.start_lineno + curr_frame.frame_lines
        )
        self._show_code(code, curr_frame.start_lineno, curr_lineno=curr_frame.curr_lineno)
    do_ll = do_longlist

    @check_args(int, None)
    def do_list(self, lineno):
        self._show_curr_frame(lineno)
    do_l = do_list

    @check_args(int, 1)
    def do_up(self, count):
        self.curr_frame_idx = self.curr_frame_idx + count
        if self.curr_frame_idx > len(self.curr_film.frames) - 1:
            self.info("Already at oldest frame")
            self.curr_frame_idx = len(self.curr_film.frames) - 1

        self.curr_frame = self.curr_film.frames[self.curr_frame_idx]
        self._show_curr_frame()
    do_u = do_up

    @check_args(int, 1)
    def do_down(self, count):
        self.curr_frame_idx = self.curr_frame_idx - count
        if self.curr_frame_idx < 0:
            self.info("Already at newest frame")
            self.curr_frame_idx = 0

        self.curr_frame = self.curr_film.frames[self.curr_frame_idx]
        self._show_curr_frame()
    do_d = do_down

    @check_args(int, 1)
    def do_next(self, step):
        if not self._switch_film(self.curr_film_idx + step):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_n = do_next

    @check_args(int, 1)
    def do_back(self, step):
        if not self._switch_film(self.curr_film_idx - step):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_b = do_back

    @check_args(None, None)
    def do_where(self):
        for frame in self.curr_film.frames[::-1]:
            file_string = f"{frame.filename}({frame.curr_lineno}):{frame.co_name}"
            code_string = self.viewer.get_source_line(
                frame.filename,
                frame.curr_lineno
            )
            if frame == self.curr_frame:
                self.message(f"* {file_string}")
            else:
                self.message(f"  {file_string}")
            self.message(f"  > {code_string.strip()}")
    do_w = do_where

    @check_args(str, None)
    def do_print(self, val):
        if val is None:
            self.info("Usage: p <arg>")
        try:
            self.message(self._get_val(val))
        except Exception as e:
            self.info("".join(traceback.format_exception_only(type(e), e)), end="")
    do_p = do_print

    def do_quit(self, args):
        return True
    do_q = do_exit = do_quit


def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("progshot_file", nargs=1)
    options = parser.parse_args(sys.argv[1:])
    filename = options.progshot_file[0]
    cli = CLI(filename)
    cli.run()


if __name__ == '__main__':
    cli_main()
