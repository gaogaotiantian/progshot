# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import io
from progshot import shoot, dump


class BenchmarkCase:
    def __init__(self):
        self.s = io.StringIO()
        self.big_string = "abc"*1000
        self.big_dict = {f"{i}": i for i in range(20)}

    def do_baseline(self):
        self.many_local_changes()

    def do_experiment(self):
        with shoot(depth=2):
            self.many_local_changes()

    def do_dump(self):
        films = dump()
        return films

    def many_local_changes(self):
        for _ in range(20):
            a = 1
            b = 2
            c = 3
            d = 4
            e = 5
            f = 6



bm = BenchmarkCase()
do_baseline = bm.do_baseline
do_experiment = bm.do_experiment
do_dump = bm.do_dump