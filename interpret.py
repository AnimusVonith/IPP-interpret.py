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
        6: "context err",
        7: "semantic err",
        8: "command err"
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
    if checked_word != "program" and checked_word != "instruction" and match('arg[1-4]', checked_word) == 0:
        err_exit(6)
    elif checked_word == "program" and context != []:
        err_exit(6)
    elif len(context) == 0 and checked_word != "program":
        err_exit(6)
    elif checked_word == "instruction" and context == [-1]:
        err_exit(6)
    elif match('arg[1-4]', checked_word) and context[-1] != "instruction":
        err_exit(6)
    context.append(checked_word)



def context_exit(checked_word):
    if len(context) == 0:
        err_exit(6)
    elif context[-1] == checked_word:
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

instruction_list = []
instruction_with_args=[]

for line in source_file.readlines():
    if search('<program language=".+" name=".+">$',line):
        if match(compile('ippcode20' ,IGNORECASE),line.split(' ')[1].split('=')[1]):
            err_exit(7)
        context_entry("program")

    elif search('<instruction order="[1-9][0-9]*" opcode=".+">$' ,line):
        context_entry("instruction")
        instruction_with_args=[]
        instruction = [line.strip().split(' ')[1].split('=')[1].strip('"'),
                       line.strip().split(' ')[2].split('=')[1].split('>')[0].strip('"')]
        instruction_with_args.append(instruction)

    elif search('<arg[1-4] type=.+>.*</arg[1-4]>$' ,line):
        if line.strip()[4] != line.strip()[-2]:
            err_exit(7)
        context_entry("arg" +str(line.strip()[4]))
        argument = [line.strip()[4],
                    line.strip().split(' ')[1].split('>')[0].split('=')[1].strip('"'),
                    line.strip().split(' ')[1].split('>')[1].split('<')[0]]

        instruction_with_args.append(argument)
        context_exit("arg" +str(line.strip()[-2]))

    elif search('</instruction>$' ,line):
        context_exit("instruction")
        instruction_list.append(instruction_with_args)
    elif search('</program>$' ,line):
        context_exit("program")
    else:
        err_exit(8)

def sorting_func(e):
    return int(e[0][0])

instruction_list.sort(key=sorting_func)
for i in instruction_list:
    print(i)

exit(0)
