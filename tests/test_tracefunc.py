# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import dis
import inspect
import progshot
from progshot.film import Film
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

        # For sys.settrace, if "call" returns None, then "return" will never
        # trigger, so we can keep count of depth. For sys.profile, "call"
        # and "return" will always trigger, so we set curr_depth to a larger
        # value
        tf = TraceFunc(capture=p.capture, depth=8, outer=0, curr_depth=6)
        sys.setprofile(tf)
        # Trigger the trace function
        p.config(save_at_exit=False)
        # sanity check for setprofile
        stub()
        sys.setprofile(None)
        # call to stub will not be captured, only return
        self.assertEqual(len(p._films), 1)

        p = progshot.ProgShot(save_at_exit=False)

        frames = inspect.getouterframes(inspect.currentframe())
        tf = TraceFunc(capture=p.capture, depth=10, outer=0, curr_depth=8)
        sys.setprofile(tf)
        _ = Film(frames[-1:])
        sys.setprofile(None)
        self.assertGreater(len(p._films), 30)

    def test_is_ins_local(self):
        p = progshot.ProgShot(save_at_exit=False)
        tf = TraceFunc(capture=p.capture, depth=1, outer=0)
        self.assertTrue(all([tf._is_ins_local(ins) for ins in dis.get_instructions("a = 2")]))
        self.assertFalse(all([tf._is_ins_local(ins) for ins in dis.get_instructions("a[3] = 2")]))
