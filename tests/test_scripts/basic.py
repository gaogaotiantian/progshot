from progshot import capture


def func_f(i):
    a = 3
    b = {"c": 5}
    capture()
    return a + b["c"]


def func_g(i):
    func_f(i)


for i in range(10):
    func_g(i)
