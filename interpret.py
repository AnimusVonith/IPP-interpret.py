#!/usr/bin/python

import sys
import re

no_err=0
err=1
input=""
source=""

def err_exit(err_code):
    switcher = {
        1: "par len err",
        2: "help err",
        3: "else err"
    }
    print(switcher.get(err_code, "Error in error printing"))
    exit(err_code)

if len(sys.argv)<2 or len(sys.argv)>3:
    err_exit(err)

for arg in sys.argv[1:]:
    if re.match('--input=.+', arg):
        input=arg.split('=')[1]
    elif re.match('--source=.+', arg):
        source=arg.split('=')[1]
    elif re.match('--help', arg):
        if len(sys.argv)>2:
            err_exit(2)
        else:
            print("WOW! This is useless\n")
            exit(no_err)
    else:
        err_exit(3)

if input == "":
    input = sys.stdin.read()
elif source == "":
    source = sys.stdin.read()

try:
    ...
except:
    ...

print("done")
exit(0)