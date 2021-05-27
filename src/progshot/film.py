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
            m = inspect.getmodule(val)
            if m and hasattr(m, "__package__") and m.__package__ == "progshot":
                # Skip the variable if it's in progshot
                continue
            if dill.pickles(val):
                self.locals[key] = val
            else:
                self.locals[key] = UnPickleable()

        self.frame_id = id(frame)
        self.filename = filename
        self.start_lineno = start_lineno
        self.frame_lines = frame_lines
        self.curr_lineno = curr_lineno
        self.co_name = frame.f_code.co_name


# key: (co_filename, co_first_lineno)
# val: (start_lineno, len(code))
source_file_cache = {}


class Film:
    """
    A film contains information of the whole program at a specific point
    """
    def __init__(self, frame_info, name=None):
        """
        frame_info is from either
            * inspect.getouterframes()
            OR
            * dilled bytes
        """
        self.frames = []
        if isinstance(frame_info, list):
            self.load_from_frames(frame_info)
            self.name = name
        elif isinstance(frame_info, bytes):
            self.load_from_dill(frame_info)

    def load_from_frames(self, frames):
        self.sources = set()
        for f_info in frames:
            frame = f_info.frame
            m = inspect.getmodule(frame)
            if m and hasattr(m, "__package__") and m.__package__ == "progshot":
                # Skip the frame if it's in progshot
                continue
            filename = os.path.abspath(f_info.filename)
            cached_data = source_file_cache.get((frame.f_code.co_filename, frame.f_code.co_firstlineno), None)
            if cached_data is None:
                try:
                    lines, start_lineno = inspect.getsourcelines(f_info.frame)
                    if start_lineno == 0:
                        # If the frame is a module, getsourcelines return 0 as
                        # start lineno. However this does not conform to what
                        # we expect. We make it 1 to be compatible
                        start_lineno = 1
                    frame_lines = len(lines)
                except OSError:
                    # If we can't get source, use start_lineno = -1 as indicator
                    start_lineno = -1
                    frame_lines = 0
                source_file_cache[(frame.f_code.co_filename, frame.f_code.co_firstlineno)] = (start_lineno, frame_lines)
            else:
                start_lineno, frame_lines = cached_data

            self.frames.append(Frame(
                frame=f_info.frame,
                filename=filename,
                start_lineno=start_lineno,
                frame_lines=frame_lines,
                curr_lineno=f_info.lineno
            ))
            self.sources.add(filename)

    def load_from_dill(self, dill_raw):
        data = dill.loads(dill_raw)
        self.frames = data["frames"]
        self.name = data["name"]

    def dumps(self):
        return dill.dumps({
            "frames": self.frames,
            "name": self.name
        })
