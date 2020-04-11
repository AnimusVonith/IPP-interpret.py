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
        8: "command err",
        9: "list err",
        10: "instr_err",
        11: "arg err",
        12: "var err"
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

instruction_list = {}
instruction_with_args=[]

for line in source_file.readlines():
    if search('<program language=".+" name=".+">$',line):
        if match(compile('ippcode20' ,IGNORECASE),line.split(' ')[1].split('=')[1]):
            err_exit(7)
        context_entry("program")

    elif search('<instruction order="[1-9][0-9]*" opcode=".+">$' ,line):
        context_entry("instruction")
        if not line.strip().split(' ')[1].split('=')[1].strip('"') in instruction_list:
            instruction_with_args = [line.strip().split(' ')[1].split('=')[1].strip('"'),
                                 line.strip().split(' ')[2].split('=')[1].split('>')[0].strip('"')]
        else:
            err_exit(7)
    elif search('<arg[1-4] type=.+>.*</arg[1-4]>$' ,line):
        if line.strip()[4] != line.strip()[-2]:
            err_exit(7)
        context_entry("arg" +str(line.strip()[4]))


        instruction_with_args.append([line.strip()[4],
                    line.strip().split(' ')[1].split('>')[0].split('=')[1].strip('"'),
                    line.strip().split(' ')[1].split('>')[1].split('<')[0]])


        context_exit("arg" +str(line.strip()[-2]))

    elif search('</instruction>$' ,line):
        context_exit("instruction")
        instruction_list[int(instruction_with_args[0])]=instruction_with_args

    elif search('</program>$' ,line):
        context_exit("program")
    else:
        err_exit(8)


def check_n_of_args(expected_n, checked_n):
    if expected_n != checked_n:
        err_exit(11)


class Variable:
    def __init__(self, type, value):
        self.type = type
        self.value = value

frame_stack = []

global_frame = {

}

temp_frame = None
local_frames = None


frames = {
    "TF" : temp_frame,
    "LF" : local_frames,
    "GF" : global_frame
}

def var_handle(variable_string):
    return variable_string.split("@")

def get_variable(variable_string):
    frame_name, var_name = var_handle(variable_string)
    if var_name in frames[frame_name]:
        return frames[var_name]
    else:
        err_exit(12)

def check_types(target1, target2):
    if target1.type != target2.type:
        ...



def MOVE_func(pars):
    destination, target = pars
    get_variable(destination)
    ...

def CREATEFRAME_func():
    frames["TF"] = {}

def PUSHFRAME_func():
    if frames["TF"] is None:
        err_exit(55)
    if frames["LF"] is None:
        frames["LF"] = {}
    frames["LF"].append(frames["TF"]) #copy
    frames["TF"] = None

def POPFRAME_func():
    if frames["TF"] is None:
        frames["TF"] = {}
    if frames["LF"] is not None:
        try:
            frames["TF"] = frames["LF"].pop()
        except:
            ...
    else:
        err_exit(55)

def DEFVAR_func(pars):
    ...
def CALL_func(pars):
    ...
def RETURN_func():
    ...
def PUSHS_func(pars):
    ...
def POPS_func(pars):
    ...
def MATH_func(pars):
    ...
def COMPARISON_func(pars):
    ...
def LOGICAL_func(pars):
    ...
def INT2CHAR_func(pars):
    ...
def STRI2INT_func(pars):
    ...
def READ_func(pars):
    ...
def WRITE_func(pars):
    ...
def CONCAT_func(pars):
    ...
def STRLEN_func(pars):
    ...
def GETCHAR_func(pars):
    ...
def SETCHAR_func(pars):
    ...
def TYPE_func(pars):
    ...
def LABEL_func(pars):
    ...
def JUMP_func(pars):
    ...
def JUMPIF_func(pars):
    ...
def EXIT_func(pars):
    ...
def DPRINT_func(pars):
    ...
def BREAK_func():
    ...


instruction_Dictionary = {
    "MOVE" : (MOVE_func,2),
    "CREATEFRAME" : (CREATEFRAME_func,0),
    "PUSHFRAME" : (PUSHFRAME_func,0),
    "POPFRAME" : (POPFRAME_func,0),
    "DEFVAR" : (DEFVAR_func,1),
    "CALL" : (CALL_func,1),
    "RETURN" : (RETURN_func,0),
    "PUSHS" : (PUSHS_func,1),
    "POPS" : (POPS_func,1),
    "ADD" : (MATH_func,3),
    "SUB" : (MATH_func,3),
    "MUL" : (MATH_func,3),
    "IDIV" : (MATH_func,3),
    "LT" : (COMPARISON_func,3),
    "GT" : (COMPARISON_func,3),
    "EQ" : (COMPARISON_func,3),
    "AND" : (LOGICAL_func,3),
    "OR" : (LOGICAL_func,3),
    "NOT" : (LOGICAL_func,3),
    "INT2CHAR" : (INT2CHAR_func,2),
    "STRI2INT" : (STRI2INT_func,3),
    "READ" : (READ_func,2),
    "WRITE" : (WRITE_func,1),
    "CONCAT" : (CONCAT_func,3),
    "STRLEN" : (STRLEN_func,2),
    "GETCHAR" : (GETCHAR_func,3),
    "SETCHAR" : (SETCHAR_func,3),
    "TYPE" : (TYPE_func,2),
    "LABEL" : (LABEL_func,1),
    "JUMP" : (JUMP_func,1),
    "JUMPIFEQ" : (JUMPIF_func,3),
    "JUMPIFNEQ" : (JUMPIF_func,3),
    "EXIT" : (EXIT_func,1),
    "DPRINT" : (DPRINT_func,1),
    "BREAK" : (BREAK_func,0)
}


for i in sorted(instruction_list):
    if not instruction_list[i][1] in instruction_Dictionary:
        err_exit(10)

    check_n_of_args(instruction_Dictionary[instruction_list[i][1]][1], len(instruction_list[i])-2)

    if not len(instruction_list[i])-2:
        instruction_Dictionary[instruction_list[i][1]][0]()
    else:
        instruction_Dictionary[instruction_list[i][1]][0](sorted(instruction_list[i][2:]))




exit(0)
