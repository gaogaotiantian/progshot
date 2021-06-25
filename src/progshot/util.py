# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import os


dir_base_name = os.path.dirname(__file__)


def is_progshot_frame(frame):
    return frame.f_code.co_filename.startswith(dir_base_name)
