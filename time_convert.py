#!/usr/bin/python

# Imports the sys module provides a number of functions and variables that can    #
# be used to manipulate different parts of the Python runtime environment.        #
import sys
# Imports time to use for the pauses or sleep in the code                         #
import time
from time import gmtime, strftime, localtime


def door_timestamp(sec = 0):
    if sec == 0:
        sec = time.time()
    return strftime("%a, %d %b %Y %H:%M:%S PST ", time.localtime(sec))

print(door_timestamp(None))
