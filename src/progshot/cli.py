# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import argparse
import functools
import objprint
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
        self.films_count = len(self.viewer.films)
        objprint.config(color=False, depth=6)
        self._switch_film(0)

    @property
    def films(self):
        return self.viewer.films

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

        cmd_type = args[0]
        cmd_args = args[1:]

        try:
            func = getattr(self, "do_" + cmd_type)
        except AttributeError:
            return self._do_default(cmd)
        finish = func(cmd_args)
        if finish is None:
            return False
        else:
            return finish

    def _is_valid_film_idx(self, film_idx):
        return 0 <= film_idx < self.films_count

    def _is_child_or_sibling_film(self, film, allow_sibling=True):
        """
        return whether film is the child or sibling of current film
               or whether this film is captured on subcalls from the
               current film or on the same frame
        """
        if allow_sibling:
            if len(film.frames) < len(self.curr_film.frames):
                return False
        else:
            if len(film.frames) <= len(self.curr_film.frames):
                return False

        # Compare it backwards because we compare from the outermost frame
        for idx in range(-1, -len(self.curr_film.frames) - 1, -1):
            if film.frames[idx].frame_id != self.curr_film.frames[idx].frame_id:
                return False
        return True

    def _switch_frame(self, frame_idx):
        if 0 <= frame_idx < len(self.curr_film.frames):
            self.curr_frame_idx = frame_idx
            self.curr_frame = self.curr_film.frames[self.curr_frame_idx]
            return True
        return False

    def _switch_film(self, film_idx, allow_negative=False):
        # If it's a negative index, make it positive
        # Treat negative index as python counting from back
        if allow_negative and -self.films_count <= film_idx < 0:
            film_idx = self.films_count + film_idx

        if self._is_valid_film_idx(film_idx):
            self.curr_film_idx = film_idx
            self.curr_film = self.films[film_idx]
            self.curr_frame_idx = 0
            self.curr_frame = self.curr_film.frames[self.curr_frame_idx]
            return True
        return False

    def _switch_film_name(self, film_name):
        # We start from the current index because name could be duplicated
        for idx in list(range(self.curr_film_idx, self.films_count)) + list(range(0, self.curr_film_idx)):
            film = self.films[idx]
            if film.name == film_name:
                return self._switch_film(idx)
        return False

    def _switch_film_frame(self, backward=False, allow_same=True, until_line=None):
        """
        Switch to the next or previous film that is not the children of
        current film.

        If allow_same is True, switch to the same frame if possible.
        If allow_same is False, switch to the parent frame (return)

        if until_line is not None, go until
            current line number >= until_line if not backward or
            current line number <= until_line if backward
        or return from the current frame

        This is used for n/b/r/rb/unt/untb
        If such film does not exist, switch to +1/-1
        """
        if backward:
            step = -1
        else:
            step = 1
        film_idx = self.curr_film_idx + step
        while self._is_valid_film_idx(film_idx):
            if until_line is not None:
                assert(allow_same)
                # If it's out of the frame, then we are done
                if not self._is_child_or_sibling_film(self.films[film_idx], allow_sibling=True):
                    break
                # If it's in the same frame, and reached the until_line, we are done
                if not self._is_child_or_sibling_film(self.films[film_idx], allow_sibling=False):
                    if (backward and self.films[film_idx].frames[0].curr_lineno <= until_line) or \
                            (not backward and self.films[film_idx].frames[0].curr_lineno >= until_line):
                        break
            else:
                if not self._is_child_or_sibling_film(self.films[film_idx], allow_sibling=not allow_same):
                    break
            film_idx += step

        return self._switch_film(film_idx)

    def _switch_film_out_frame(self, backward=False):
        return self._switch_film_frame(backward=backward, allow_same=False)

    def _switch_film_same_frame(self, backward=False):
        return self._switch_film_frame(backward=backward, allow_same=True)

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
        self.info(f"==== Film {self.curr_film_idx + 1}/{self.films_count} - {self.curr_film.name} ====")
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
        self.info(f"Unknown syntax {args}")
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
    def do_step(self, step):
        if not self._switch_film(self.curr_film_idx + step):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_s = do_step

    @check_args(int, 1)
    def do_stepback(self, step):
        if not self._switch_film(self.curr_film_idx - step):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_sb = do_stepback

    @check_args(None, None)
    def do_next(self):
        if not self._switch_film_same_frame(backward=False):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_n = do_next

    @check_args(None, None)
    def do_back(self):
        if not self._switch_film_same_frame(backward=True):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_b = do_back

    @check_args(None, None)
    def do_return(self):
        if not self._switch_film_out_frame(backward=False):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_r = do_return

    @check_args(None, None)
    def do_returnback(self):
        if not self._switch_film_out_frame(backward=True):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_rb = do_returnback

    @check_args(int, None)
    def do_until(self, until_line):
        if until_line is None:
            until_line = self.curr_film.frames[0].curr_lineno + 1

        if not self._switch_film_frame(until_line=until_line):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_unt = do_until

    @check_args(int, None)
    def do_untilback(self, until_line):
        if until_line is None:
            until_line = self.curr_film.frames[0].curr_lineno - 1

        if not self._switch_film_frame(backward=True, until_line=until_line):
            self.error("Target film is out of range")
            return
        self._show_curr_frame()
    do_untb = do_untilback

    @check_args(str, None)
    def do_goto(self, bookmark):
        """
        bookmark could be a string for name or an 1-index
        """
        if bookmark is None:
            self.info("Usage: g <film index or film name>")
            return
        try:
            bookmark = int(bookmark)
            if bookmark >= 1:
                bookmark -= 1
            if not self._switch_film(bookmark, allow_negative=True):
                self.error("Target film does is out of range")
                return
        except ValueError:
            if not self._switch_film_name(bookmark):
                self.error(f"Could not find film '{bookmark}'")
                return
        self._show_curr_frame()
    do_g = do_goto

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

    @check_args(int, 1)
    def do_frame(self, frame_idx):
        """
        frame_idx is an 1-index
        """
        if not self._switch_frame(frame_idx - 1):
            self.error("target frame is out of range")
            return
        self._show_curr_frame()

    @check_args(str, None)
    def do_print(self, val):
        if val is None:
            self.info("Usage: p <arg>")
        try:
            self.message(self._get_val(val))
        except Exception as e:
            self.info("".join(traceback.format_exception_only(type(e), e)), end="")
    do_p = do_print

    @check_args(str, None)
    def do_pprint(self, val):
        if val is None:
            self.info("Usage: pp <arg>")
        try:
            self.message(objprint.objstr(self._get_val(val)))
        except Exception as e:
            self.info("".join(traceback.format_exception_only(type(e), e)), end="")
    do_pp = do_pprint

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
