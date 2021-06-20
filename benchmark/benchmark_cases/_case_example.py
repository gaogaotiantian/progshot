# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt

# This is the minumim example for a benchmark case
# Each benchmark is a .py file, which has the following functions
#   - do_init
#   - do_baseline
#   - do_experiment
#   - do_dump


# Normally you need either capture or trace or shoot, plus dump
from progshot import shoot, dump


# Do all the initialization, this function can be omitted
def do_init():
    pass


# Do the baseline function for performance reference
def do_baseline():
    a = 1


# Do the function with progshot
def do_experiment():
    with shoot():
        a = 1


# Do the dump and return the number of films
def do_dump():
    films = dump()
    return films
