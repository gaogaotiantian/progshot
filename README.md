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

``progshot`` will automatically save the captures as ``out.pshot``

### View

To view the report, you can use CLI or Web interface.

#### CLI

```
psview out.pshot
```

The CLI interface is similar to pdb. You can use commands that have the same meaning in pdb

<details>
<summary>psview commands</summary>

* p expression - print evaluate of expression
* w(here) - show stack trace
* u(p) [_count_] - move the current frame _count_ levels up (to older frame)
* d(own) [_count_] - move the current frame _count_ levels down (to later frame)
* n(ext) [_count_] - go to _count_ films(capture) after
* b(ack) [_count_] - go to _count_ films(capture) before
* l(ist) [_lineno_] - show source code around _lineno_
* ll - show full source code of existing frame

</details>