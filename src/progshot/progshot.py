# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import atexit
import dill
import functools
import inspect
import sys
from .film import Film


class TraceFunc:
    def __init__(self, capture, depth, outer=0):
        self.depth = depth
        self.curr_depth = 0
        self.outer = outer
        self.capture = capture

    def __call__(self, frame, event, arg):
        if event == "call":
            if self.curr_depth >= self.depth:
                return None
            self.curr_depth += 1
            return self
        elif event == "line":
            self.capture(frame=frame, outer=self.curr_depth + self.outer - 1)
        elif event == "return":
            self.capture(frame=frame, outer=self.curr_depth + self.outer - 1)
            self.curr_depth -= 1


class ProgShot:
    def __init__(self, **kwargs):
        self._file = "./out.pshot"
        self._films = []
        self._sources = {}
        self._save_at_exit = True
        self._trace_config = {
            "depth": 1
        }
        atexit.register(self.dump)
        self.config(**kwargs)

    def _is_progshot_frame(self, frame):
        m = inspect.getmodule(frame)
        return m and hasattr(m, "__package__") and m.__package__ == "progshot"

    def capture(self, name=None, frame=None, outer=None):
        """
        name: str
            - name of of this capture(film), if None, use
              default name Film-<num>
        frame: Frame
            - the frame to capture, if None, capture the caller of this function
        outer: integer
            - how many frames to capture outside of the capture frame
              if None, all of them
        """
        if frame is None:
            frame = inspect.currentframe().f_back

        if self._is_progshot_frame(frame):
            # We don't capture frames inside progshot
            del frame
            return

        outer_frames = inspect.getouterframes(frame)
        outer_frames = [frame for frame in outer_frames if not self._is_progshot_frame(frame)]

        if outer is not None:
            assert(outer >= 0)
            outer_frames = outer_frames[:outer + 1]

        if name is None:
            name = f"Film-{len(self._films) + 1}"

        new_film = Film(outer_frames, name=name)

        for source in new_film.sources:
            if source not in self._sources:
                try:
                    with open(source) as f:
                        self._sources[source] = f.read()
                except OSError:
                    self._sources[source] = None
        self._films.append(new_film.dumps())
        del outer_frames

    def trace(self, method=None, depth=None, outer=0):

        if depth is None:
            depth = self._trace_config["depth"]

        def inner(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                prev_trace_func = sys.gettrace()
                sys.settrace(TraceFunc(self.capture, depth, outer=outer))
                ret = func(*args, **kwargs)
                sys.settrace(prev_trace_func)
                return ret

            return wrapper

        if method:
            return inner(method)
        return inner

    def dump(self, filename=None, clear_data=True):
        if filename is None:
            filename = self._file
        if self._films:
            with open(filename, "wb") as f:
                dill.dump({
                    "sources": self._sources,
                    "films": self._films
                }, f)

        if clear_data:
            self._films = []
            self._sources = {}

    def config(self, **kwargs):
        for key, val in kwargs.items():
            if key == "save_at_exit":
                if self._save_at_exit and val is False:
                    atexit.unregister(self.dump)
                    self._save_at_exit = False
                elif not self._save_at_exit and val is True:
                    atexit.register(self.dump)
                    self._save_at_exit = True
                elif val not in (True, False):
                    raise TypeError(f"save_at_exit should be True or False, not {val}")
            elif key == "depth":
                try:
                    self._trace_config["depth"] = int(val)
                except ValueError:
                    raise ValueError(f"depth can only be integer, not {val}")
            elif key == "filename":
                if isinstance(val, str):
                    self._file = val
                else:
                    raise ValueError(f"filename can only be string, not {val}")

    def __reduce__(self):
        # To make sure if this object is accidentally pickled, the file size won't
        # go crazy because recursively including ._films
        return (ProgShot, tuple())
