# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import atexit
import dill
import dis
import functools
import inspect
import sys
from .film import Film
from .util import is_progshot_frame


class TraceFunc:
    def __init__(self, capture, depth, outer=0, curr_depth=0):
        self.depth = depth
        self.curr_depth = curr_depth
        self.outer = outer
        self.capture = capture
        self.pickled_objects = {}

    def __call__(self, frame, event, arg):
        if event == "call":
            self.pickled_objects = {}
            if self.curr_depth >= self.depth:
                return None
            self.curr_depth += 1
            return self
        elif event == "line":
            self.capture(frame=frame, outer=self.curr_depth + self.outer - 1, pickled_objects=self.pickled_objects)
            if not self._local_change(frame):
                self.pickled_objects = {}
        elif event == "return":
            self.capture(frame=frame, outer=self.curr_depth + self.outer - 1, pickled_objects=self.pickled_objects)
            self.curr_depth -= 1

    def _get_line_instructions(self, frame):
        starts_line = frame.f_lineno
        line_started = False
        instructions = []
        for ins in dis.get_instructions(frame.f_code):
            if not line_started:
                if ins.starts_line == starts_line:
                    line_started = True
                    instructions.append(ins)
            else:
                if ins.starts_line is not None:
                    break
                instructions.append(ins)
        return instructions

    def _local_change(self, frame):
        for ins in self._get_line_instructions(frame):
            if not self._is_ins_local(ins):
                return False
        return True

    def _is_ins_local(self, ins):
        if ins.opname.startswith("CALL_"):
            return False
        elif ins.opname.startswith("STORE_"):
            if ins.opname not in ("STORE_NAME", "STORE_FAST"):
                return False
        return True


class PSContext:
    def __init__(self, capture, depth, outer):
        self.capture = capture
        self.depth = depth
        self.outer = outer
        self.prev_trace_func = None

    def __enter__(self):
        call_frame = inspect.currentframe().f_back
        self.prev_trace_func = sys.gettrace()
        call_frame.f_trace = TraceFunc(self.capture, self.depth, outer=self.outer, curr_depth=1)
        sys.settrace(call_frame.f_trace)

    def __exit__(self, exc_type, exc_value, traceback):  # pragma: no cover
        sys.settrace(self.prev_trace_func)
        call_frame = inspect.currentframe().f_back
        call_frame.f_trace = self.prev_trace_func


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

    def capture(self, name=None, frame=None, outer=None, pickled_objects={}):
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

        if is_progshot_frame(frame):  # pragma: no cover
            # We don't capture frames inside progshot
            del frame
            return

        outer_frames = inspect.getouterframes(frame)
        outer_frames = [frame_info for frame_info in outer_frames if not is_progshot_frame(frame_info.frame)]

        if outer is not None:
            assert(outer >= 0)
            outer_frames = outer_frames[:outer + 1]

        if name is None:
            name = f"Film-{len(self._films) + 1}"

        new_film = Film(outer_frames, name=name, pickled_objects=pickled_objects)

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

    def shoot(self, depth=None, outer=0):
        if depth is None:
            depth = self._trace_config["depth"]
        return PSContext(self.capture, depth, outer)

    def dump(self, filename=None, clear_data=True):
        if filename is None:
            filename = self._file
        if self._films:
            with open(filename, "wb") as f:
                dill.dump({
                    "sources": self._sources,
                    "films": self._films
                }, f)

        dumped_films = len(self._films)
        if clear_data:
            self._films = []
            self._sources = {}

        return dumped_films

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
        return "_pshot"


_pshot = ProgShot()
