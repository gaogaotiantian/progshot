from progshot import trace


class Data:
    def __init__(self):
        self.a = 1
        self.b = {"a": 2, "b": 3}
        self.c = [i for i in range(10)]


@trace
def func_f():
    a = Data()
    return a


func_f()
