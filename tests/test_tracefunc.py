# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import inspect
import progshot
from progshot.progshot import TraceFunc
import sys
import unittest


class TestTraceFunc(unittest.TestCase):
    def test_basic(self):
        p = progshot.ProgShot(save_at_exit=False)
        tf = TraceFunc(capture=p.capture, depth=1, outer=0)
        frame = inspect.currentframe()
        # Enter the actual call
        tf(frame, "call", None)
        tf(frame, "line", None)
        # Enter the call that's not supposed to trace
        # We should return None to turn off the trace
        local_tf = tf(frame, "call", None)
        self.assertIs(local_tf, None)
        # We returned from the call already, it's not
        # recorded because no local trace function is set
        tf(frame, "line", None)
        tf(frame, "return", None)
        self.assertEqual(len(p._films), 3)

    def test_with_profile(self):
        # It's hard to get coverage for trace function inside progshot
        # because normally it's triggered by settrace, which is used
        # by coverage.py for coverage stat. However, we can use setprofile
        # to simulate the process and get some coverage
        def stub():
            pass

        p = progshot.ProgShot(save_at_exit=False)
        tf = TraceFunc(capture=p.capture, depth=2, outer=0)
        sys.setprofile(tf)
        # Trigger the trace function
        p.config(save_at_exit=False)
        # sanity check for setprofile
        stub()
        sys.setprofile(None)
        # call to stub will not be captured, only return
        self.assertEqual(len(p._films), 1)
