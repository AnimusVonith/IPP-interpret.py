#!/usr/bin/python

from sys import stdin, argv
from re import match, compile, IGNORECASE, search

input_path = ""
source_path = ""
context = []


def err_exit(err_code):
    switch_err = {
        1: "par len err",
        2: "help err",
        3: "else err",
        4: "file err",
        5: "match err",
        6: "context err"
    }
    print(switch_err.get(err_code, "Error in error printing"))
    exit(err_code)

def path_handler(checked_path):
    if checked_path == "":
        return stdin
    else:
        try:
            return open(checked_path, 'r')
        except:
            err_exit(4)

def context_entry(checked_word):
    if checked_word != "program" or checked_word != "instruction" or match('arg[1-4]', checked_word) == 0:
        err_exit(6)
    elif checked_word == "program" and context != []:
        err_exit(6)
    elif checked_word == "instruction" and context[-1] != "program":
        err_exit(6)
    elif match('arg[1-4]', checked_word) and context[-1] != "instruction":
        err_exit(6)
    context.push(checked_word)


def context_exit(checked_word):
    if context[-1] == checked_word:
        context.pop()
    else:
        err_exit(6)


if len(argv) < 2 or len(argv) > 3:
    err_exit(1)

for arg in argv[1:]:
    if match('--input\=.+', arg):
        input_path = arg.split('=')[1]
    elif match('--source\=.+', arg):
        source_path = arg.split('=')[1]
    elif match('--help', arg):
        if len(argv) > 2:
            err_exit(2)
        else:
            print("WOW! This is useless\n")
            exit(0)
    else:
        err_exit(3)


input_file=path_handler(input_path)
source_file=path_handler(source_path)


if match('<\?xml version="1.0" encoding="UTF-8"\?>', source_file.readline()) == 0:
    err_exit(5)


for line in source_file.readlines():
    if search('<program language=".+" name=".+">',line):
        print("program")
    elif search('<instruction order="[1-9][0-9]*" opcode=".+">',line):
        print("instruction")
    elif search('<arg[1-4] type=.+>',line):
        print("arg")
    else:
        print(line)

print("done")
exit(0)
