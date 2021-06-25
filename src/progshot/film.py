# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import dill
import inspect
import os
from .util import is_progshot_frame


class UnPickleable(object):
    pass


class Frame:
    def __init__(self, frame, filename, start_lineno, frame_lines, curr_lineno, object_dict):
        self.locals = {}
        assert(not is_progshot_frame(frame))
        for key, val in frame.f_locals.items():
            val_id = id(val)
            self.locals[key] = val_id
            if val_id not in object_dict:
                object_dict[id(val)] = val

        self.frame_id = id(frame)
        self.filename = filename
        self.start_lineno = start_lineno
        self.frame_lines = frame_lines
        self.curr_lineno = curr_lineno
        self.co_name = frame.f_code.co_name

    def _decode(self, object_dict):
        # convert self.locals back to normal object from id
        for key in self.locals:
            val_id = self.locals[key]
            self.locals[key] = object_dict[val_id]


# key: (co_filename, co_first_lineno)
# val: (start_lineno, len(code))
source_file_cache = {}


class Film:
    """
    A film contains information of the whole program at a specific point
    """
    def __init__(self, frame_info, name=None, pickled_objects={}):
        """
        frame_info is from either
            * inspect.getouterframes()
            OR
            * dilled bytes
        """
        self.frames = []
        # key: id, val: object
        self.objects = {}
        self.pickled_objects = pickled_objects
        if isinstance(frame_info, list):
            self.load_from_frames(frame_info)
            self.name = name
        elif isinstance(frame_info, bytes):
            self.load_from_dill(frame_info)

    def load_from_frames(self, frames):
        self.sources = set()
        for f_info in frames:
            frame = f_info.frame
            if is_progshot_frame(frame):
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
                curr_lineno=f_info.lineno,
                object_dict=self.objects
            ))
            self.sources.add(filename)

        for obj_id, obj in self.objects.items():
            if obj_id not in self.pickled_objects:
                try:
                    self.pickled_objects[obj_id] = dill.dumps(obj)
                except Exception:
                    self.pickled_objects[obj_id] = dill.dumps(UnPickleable())

    def load_from_dill(self, dill_raw):
        data = dill.loads(dill_raw)
        self.frames = data["frames"]
        self.name = data["name"]
        self.pickled_objects = data["objects"]
        for obj_id, obj in self.pickled_objects.items():
            self.objects[obj_id] = dill.loads(obj)
        for frame in self.frames:
            frame._decode(self.objects)

    def dumps(self):
        return dill.dumps({
            "frames": self.frames,
            "name": self.name,
            "objects": self.pickled_objects
        })
