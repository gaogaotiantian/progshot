# progshot
[![build](https://github.com/gaogaotiantian/progshot/workflows/build/badge.svg)](https://github.com/gaogaotiantian/progshot/actions?query=workflow%3Abuild)  [![flake8](https://github.com/gaogaotiantian/progshot/workflows/lint/badge.svg)](https://github.com/gaogaotiantian/progshot/actions?query=workflow%3ALint)  [![coverage](https://img.shields.io/codecov/c/github/gaogaotiantian/progshot)](https://codecov.io/gh/gaogaotiantian/progshot)  [![pypi](https://img.shields.io/pypi/v/progshot.svg)](https://pypi.org/project/progshot/)  [![support-version](https://img.shields.io/pypi/pyversions/progshot)](https://img.shields.io/pypi/pyversions/progshot)  [![license](https://img.shields.io/github/license/gaogaotiantian/progshot)](https://github.com/gaogaotiantian/progshot/blob/master/LICENSE)

progshot is a debugging tool that enables "offline-debugging" for your python program.

[![example_img](https://github.com/gaogaotiantian/progshot/blob/master/img/example.png)](https://github.com/gaogaotiantian/progshot/blob/master/img/example.png)

## Install

```
pip install progshot
```

## Usage

### Trace

To capture a continuous run and be able to offline debug it like a real debugger, use ``@trace``

```python
from progshot import trace

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

@trace
def bubbleSort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                swap(arr, j, j + 1)
```

``@trace`` will record every line executed in the decorated function and generated a ``out.pshot`` file. With ``psviewer``,
you can enjoy a debugger-like environment offline, where you can not only go forward, but go backward as well.

Each capture is called a **film**, which contains all the frames the local variables in them.

By default, ``@trace`` is not recursive, but you can set the ``depth`` of ``@trace``

```python
from progshot import trace

def swap(arr, i, j):
    # Now this function will be recorded as well
    arr[i], arr[j] = arr[j], arr[i]

@trace(depth=2)
def bubbleSort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                swap(arr, j, j + 1)
```

### View

To view the report, you can use Web interface or CLI.

#### Web

```
psview out.pshot
```

#### CLI

```
psview-cli out.pshot
```

Web interface also provides a terminal which behaves like the CLI.

The CLI interface is similar to pdb. You can use commands that have the similar meanings in pdb, except
that you have a set of "backward debugging" commands.

<details>
<summary>psview commands</summary>

* p _expression_ - print eval of expression
* pp _expression_ - pretty print eval of expression with `objprint`
* w(here) - show stack trace
* u(p) [_count_] - move the current frame _count_ levels up (to older frame)
* d(own) [_count_] - move the current frame _count_ levels down (to later frame)
* n(ext) - go to next line in current function if possible, otherwise next film
* b(ack) - go to previous line in current function if possible, otherwise previous film
* s(tep) - go to next film
* s(tep)b(ack) - go to previous film
* r(eturn) - go to the next film when the current function returns
* r(eturn)b(ack) - go to the previous film before the current function enters
* unt(il) [_lineno_] - go forward until the line with a number that's >= _lineno_ is reached
* unt(il)b(ack) [_lineno_] - go backward until the line with a number that's <= _lineno_ is reached
* g(oto) [_bookmark_] - goto _bookmark_ film. _bookmark_ can be film index or film name
* l(ist) [_lineno_] - show source code around _lineno_
* ll - show full source code of existing frame

</details>

### Single Capture

You can also use ``capture`` function to do a single capture.

```python
from progshot import capture

def add(a, b):
    capture()
    return a + b
```

<details>

<summary> You can give a name(bookmark) for the capture to switch to the film quickly </summary>

Do not use space in ``name``

```python
from progshot import capture

def add(a, b):
    capture(name="cap_in_add")
    return a + b
```

</details>

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/gaogaotiantian/progshot/issues).

## License

Copyright Tian Gao, Mengjia Zhao, 2021.

Distributed under the terms of the  [Apache 2.0 license](https://github.com/gaogaotiantian/progshot/blob/master/LICENSE).
