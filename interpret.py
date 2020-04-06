#!/usr/bin/python

import sys
import re

input_path=""
source_path=""
context=[]

def err_exit(err_code):
    switcher = {
        1: "par len err",
        2: "help err",
        3: "else err",
        4: "file err",
        5: "match err",
        6: "context err"
    }
    print(switcher.get(err_code, "Error in error printing"))
    exit(err_code)

def context_entry(checked_word):
    if checked_word == "program" and context != []:
        err_exit(6)
    if context[-1] == checked_word or re.match(checked_word+'[1-9][0-9]*', context[-1]):
        err_exit(6)


def context_exit(checked_word):
    last_context = context.pop()
    if re.match('arg[1-9][0-9]*', checked_word) == 0:
        ...
    if checked_word != "instruction":
        ...
    if checked_word != "program":
        ...

    if last_context == checked_word:
        ...


if len(sys.argv)<2 or len(sys.argv)>3:
    err_exit(err)

for arg in sys.argv[1:]:
    if re.match('--input\=.+', arg):
        input_path=arg.split('=')
    elif re.match('--source\=.+', arg):
        source_path=arg.split('=')[1]
    elif re.match('--help', arg):
        if len(sys.argv)>2:
            err_exit(2)
        else:
            print("WOW! This is useless\n")
            exit(no_err)
    else:
        err_exit(3)

if input_path == "":
    input_path = "sys.stdin"
if source_path == "":
    source_path = "sys.stdin"

source_file = open(source_path, 'r')
if re.match('<\?xml version="1.0" encoding="UTF-8"\?>',source_file.readline()) == 0:
    err_exit(5)

for line in source_file.readlines():
    print(line, end="")


print("done")
exit(0)