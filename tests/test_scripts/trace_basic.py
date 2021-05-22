from progshot import trace
import random


def func_f(i):
    a = 3
    b = {"c": 5}
    c = random.random()
    return a + b["c"] + c


@trace(depth=3)
def func_g(i):
    for _ in range(3):
        func_f(i)


@trace
def func_h():
    a = 4
    return a


for i in range(5):
    func_g(i)
func_h()
