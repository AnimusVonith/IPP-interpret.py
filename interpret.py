#!/usr/bin/python

import sys
import re

no_err=0
err=1
input=""
source=""

if 1>len(sys.argv)>2:
    exit(err)

def err_exit(err_code):
    switcher = {
        1: "Error occured"
    }
    print(switcher.get(err_code, "Error in error printing"))
    exit(err_code)

for arg in sys.argv:
    if re.match('--input=.+', arg):
        input=arg.split('=')[1]
    elif re.match('--source=.+', arg):
        source=arg.split('=')[1]
    elif re.match('--help', arg):
        if len(sys.argv)>1:
            err_exit(err)
        else:
            print("WOW! This is useless\n")
            exit(no_err)
    else:
        err_exit(err)

if input == "":
    input = sys.stdin.read()
elif source == "":
    source = sys.stdin.read()
