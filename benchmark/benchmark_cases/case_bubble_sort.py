# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


from progshot import shoot, dump
import random


class BenchmarkCase:
    def __init__(self):
        self.arr1 = [random.randint(0, 10000) for _ in range(20)]
        self.arr2 = self.arr1[:]

    def do_baseline(self):
        self.bubble_sort(self.arr1)

    def do_experiment(self):
        with shoot(depth=2):
            self.bubble_sort(self.arr2)

    def do_dump(self):
        films = dump()
        return films

    def swap(self, arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]

    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    self.swap(arr, j, j + 1)


bm = BenchmarkCase()
do_baseline = bm.do_baseline
do_experiment = bm.do_experiment
do_dump = bm.do_dump
