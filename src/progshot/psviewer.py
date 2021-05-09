# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import dill
from .film import Film


class ProgShotViewer:
    def __init__(self, file):
        with open(file, "rb") as f:
            data = dill.load(f)
            self.films = [Film(raw) for raw in data["films"]]
            self.sources = data["sources"]

    def get_source_lines(self, filename, start_lineno, end_lineno):
        if filename not in self.sources:
            return "Unable to get source code"
        lines = self.sources[filename].split("\n")
        start_lineno = max(1, start_lineno)
        end_lineno = min(len(lines) + 1, end_lineno)
        return '\n'.join(lines[start_lineno - 1: end_lineno - 1])

    def get_source_line(self, filename, lineno):
        return self.get_source_lines(filename, lineno, lineno + 1)

    def get_source(self, filename):
        return self.sources[filename]
