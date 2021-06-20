# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt

__version__ = "0.0.1"

from .progshot import _pshot, ProgShot
from .cli import cli_main
from .serverbooter import web_server_main


capture = _pshot.capture
config = _pshot.config
trace = _pshot.trace
dump = _pshot.dump
shoot = _pshot.shoot

__all__ = [
    "capture",
    "config",
    "cli_main",
    "trace",
    "dump",
    "shoot",
    "ProgShot",
    "web_server_main"
]
