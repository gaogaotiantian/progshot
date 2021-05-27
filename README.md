# progshot
[![build](https://github.com/gaogaotiantian/progshot/workflows/build/badge.svg)](https://github.com/gaogaotiantian/progshot/actions?query=workflow%3Abuild)  [![flake8](https://github.com/gaogaotiantian/progshot/workflows/lint/badge.svg)](https://github.com/gaogaotiantian/progshot/actions?query=workflow%3ALint)  [![coverage](https://img.shields.io/codecov/c/github/gaogaotiantian/progshot)](https://codecov.io/gh/gaogaotiantian/progshot)  [![pypi](https://img.shields.io/pypi/v/progshot.svg)](https://pypi.org/project/progshot/)  [![support-version](https://img.shields.io/pypi/pyversions/progshot)](https://img.shields.io/pypi/pyversions/progshot)  [![license](https://img.shields.io/github/license/gaogaotiantian/progshot)](https://github.com/gaogaotiantian/progshot/blob/master/LICENSE)

progshot is a debugging tool that enables "offline-debugging" for your python program.

## Install

```
pip install progshot
```

## Usage

### Capture

To capture the states of your program, use ``capture`` function.

```python
from progshot import capture

def add(a, b):
    capture()
    return a + b
```

In ``progshot``, we call a capture that has all the frame information at that time a **film**.

``progshot`` will automatically save all the captures as ``out.pshot``

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

### Trace

To capture a continuous run and be able to offline debug it like a real debugger, use ``@trace``

```python
from progshot import trace

@trace
def f(a, b):
    c = a + b
    b = c * a
    return c - b
```

``@trace`` will record every line executed in the decorated function and provide a debugger-like
environment offline, where you can not only step forward, but go backward as well.

By default, ``@trace`` is not recursive, but you can set the ``depth`` of ``@trace``

```python
from progshot import trace

def g(n):
    # this function will be recorded as well
    return n * n

@trace(depth=2)
def f(a, b):
    c = a + b
    b = c * a
    return g(c) + g(b)
```

### View

To view the report, you can use CLI or Web interface.

#### CLI

```
psview out.pshot
```

The CLI interface is similar to pdb. You can use commands that have the same meaning in pdb

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
