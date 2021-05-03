# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import dill
import inspect
import os


class UnPickleable(object):
    pass


class Frame:
    def __init__(self, frame, filename, start_lineno, frame_lines, curr_lineno):
        self.locals = {}
        for key, val in frame.f_locals.items():
            try:
                if dill.pickles(val):
                    self.locals[key] = val
                else:
                    self.locals[key] = UnPickleable()
            except Exception:
                self.locals[key] = UnPickleable()

        self.filename = filename
        self.start_lineno = start_lineno
        self.frame_lines = frame_lines
        self.curr_lineno = curr_lineno
        self.co_name = frame.f_code.co_name


class Film:
    """
    A film contains information of the whole program at a specific point
    """
    def __init__(self, frame_info):
        """
        frame_info is from either
            * inspect.getouterframes()
            OR
            * dilled bytes
        """
        self.frames = []
        if isinstance(frame_info, list):
            self.load_from_frames(frame_info)
        elif isinstance(frame_info, bytes):
            self.load_from_dill(frame_info)

    def load_from_frames(self, frames):
        self.sources = set()
        for f_info in frames:
            filename = os.path.abspath(f_info.filename)
            lines, start_lineno = inspect.getsourcelines(f_info.frame)
            if start_lineno == 0:
                # If the frame is a module, getsourcelines return 0 as
                # start lineno. However this does not conform to what
                # we expect. We make it 1 to be compatible
                start_lineno = 1
            self.frames.append(Frame(
                frame=f_info.frame,
                filename=filename,
                start_lineno=start_lineno,
                frame_lines=len(lines),
                curr_lineno=f_info.lineno
            ))
            self.sources.add(filename)

    def load_from_dill(self, dill_raw):
        data = dill.loads(dill_raw)
        self.frames = data["frames"]

    def dumps(self):
        return dill.dumps({
            "frames": self.frames,
        })
