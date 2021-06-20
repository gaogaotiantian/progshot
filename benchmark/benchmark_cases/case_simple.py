# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


from progshot import capture, dump


def func_f(i):
    a = 3
    b = {"c": 5}
    capture(outer=1)
    return a + b["c"]


def func_f_baseline(i):
    a = 3
    b = {"c": 5}
    return a + b["c"]


def do_baseline():
    for i in range(10):
        func_f_baseline(i)


def do_experiment():
    for i in range(10):
        func_f(i)


def do_dump():
    films = dump()
    return films
