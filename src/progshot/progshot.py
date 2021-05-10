# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import atexit
import dill
import inspect
from .film import Film


class ProgShot:
    def __init__(self, **kwargs):
        self._file = "./out.pshot"
        self._films = []
        self._sources = {}
        self._save_at_exit = True
        atexit.register(self.dump)
        self.config(**kwargs)

    def capture(self, name=None, frame=None):
        if frame is None:
            frame = inspect.currentframe().f_back
        if name is None:
            name = f"Film-{len(self._films) + 1}"
        new_film = Film(inspect.getouterframes(frame), name=name)
        for source in new_film.sources:
            if source not in self._sources:
                try:
                    with open(source) as f:
                        self._sources[source] = f.read()
                except OSError:
                    self._sources[source] = None
        self._films.append(new_film.dumps())

    def dump(self, filename=None):
        if filename is None:
            filename = self._file
        if self._films:
            with open(filename, "wb") as f:
                dill.dump({
                    "sources": self._sources,
                    "films": self._films
                }, f)

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
