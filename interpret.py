#!/usr/bin/python

import sys
import re

no_err=0
err=1
input_path=""
source_path=""

def err_exit(err_code):
    switcher = {
        1: "par len err",
        2: "help err",
        3: "else err",
        4: "file err"
    }
    print(switcher.get(err_code, "Error in error printing"))
    exit(err_code)

def file_handler(path):
    if path != "":
        try:
            file = open(path, "r")
        except:
            err_exit(4)
        else:
            file.close()
            return file
    else:
        return sys.stdin.read()

if len(sys.argv)<2 or len(sys.argv)>3:
    err_exit(err)

for arg in sys.argv[1:]:
    if re.match('--input=.+', arg):
        input_path=arg.split('=')[1]
    elif re.match('--source=.+', arg):
        source_path=arg.split('=')[1]
    elif re.match('--help', arg):
        if len(sys.argv)>2:
            err_exit(2)
        else:
            print("WOW! This is useless\n")
            exit(no_err)
    else:
        err_exit(3)

input_file = file_handler(input_path)
source_file = file_handler(source_path)



print("done")
exit(0)