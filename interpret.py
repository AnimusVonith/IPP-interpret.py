#!/usr/bin/python

from sys import stdin, argv, stderr
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
        12: "var err",
        52: "semantic err",
        53: "wrong type in operand",
        54: "cant access var",
        55: "cant access frame",
        56: "value is missing",
        57: "wrong value of operand",
        58: "wrong operations on string"
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


class ConstantClass:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "type: '" + self.type + "' and value: '" + str(self.value) +"'"

    def __repr__(self):
        return "('" + self.type + "' , '" + str(self.value) + "')"


global_frame = {}

temp_frame = None
local_frames = None

labels=[]

frames = {
    "TF" : temp_frame,
    "LF" : local_frames,
    "GF" : global_frame
}

def var_handle(variable_string):
    return variable_string.split("@")

def check_type_var(target_type):
    if target_type != "var":
        err_exit(53)

def get_variable(target):
    check_type_var(target[1])
    frame_name, var_name = var_handle(target[2])
    if frame_name != "LF" and frame_name != "GF" and frame_name != "TF":
        err_exit(55)
    if frame_name == "LF":
        if var_name in frames[frame_name].top():
            return frames[frame_name].top()[var_name]
        else:
            err_exit(54)
    else:
        if var_name in frames[frame_name]:
            return frames[frame_name][var_name]
        else:
            err_exit(54)

def check_type_notNone(var):
    if var.type is None or var.value is None:
        err_exit(56)

def compare_types(base, compared):
    check_type_notNone(compared)
    if base.type is not None:
        if base.type != compared.type:
            err_exit(53)

def check_if_symb(checked_symb, other_type):
    other_type_regex = compile(other_type)
    if checked_symb[1] == "var":
        symb = get_variable(checked_symb)
        if search(other_type_regex, symb.type):
            return symb
        else:
            err_exit(53)
    elif search(other_type_regex, checked_symb[1]):
        return ConstantClass(checked_symb[1], checked_symb[2])
    else:
        err_exit(53)

def MOVE_func(pars):
    destination, target = pars
    destination = get_variable(destination)
    if target[1] == "var":
        target = get_variable(target)
        check_type_notNone(target)
        destination.type = target.type
        destination.value = target.value
    else:
        check_type_notNone(ConstantClass(target[1],target[2]))
        destination.type = target[1]
        destination.value = target[2]

def CREATEFRAME_func():
    frames["TF"] = {}

def PUSHFRAME_func():
    if frames["TF"] is None:
        err_exit(55)
    if frames["LF"] is None:
        frames["LF"] = []
    frames["LF"].append(frames["TF"])
    frames["TF"] = None

def POPFRAME_func():
    if frames["TF"] is None:
        frames["TF"] = {}
    if frames["LF"] is not None and frames["LF"] != []:
        frames["TF"] = frames["LF"].pop()
    else:
        err_exit(55)

def DEFVAR_func(pars):
    frame, name = var_handle(pars[0][2])
    if frame != "LF" and frame != "GF" and frame != "TF":
        err_exit(10)
    if frame == "LF":
        if name in frames[frame].top():
            err_exit(52)
        frames[frame].top()[name] = ConstantClass(None, None)
    else:
        if name in frames[frame]:
            err_exit(52)
        frames[frame][name] = ConstantClass(None, None)

def CALL_func(pars):
    ... #TODO
def RETURN_func():
    ... #TODO

data_stack = []

def PUSHS_func(pars):
    if pars[0][1] == "var":
        var=get_variable(pars[0])
        symb=ConstantClass(var.type, var.value)
    else:
        symb=ConstantClass(pars[0][1], pars[0][2])
    check_type_notNone(symb)
    data_stack.append(symb)

def POPS_func(pars):
    destination = get_variable(pars[0])
    if not data_stack:
        err_exit(56)
    popped_symb = data_stack.pop()
    destination.type = popped_symb.type
    destination.value = popped_symb.value

def MATH_func(pars, op):
    destination, n1, n2 = pars
    destination = get_variable(destination)

    n1 = check_if_symb(n1, "int")
    n2 = check_if_symb(n2, "int")

    if op=="ADD":
        destination.value = int(n1.value) + int(n2.value)
    elif op=="SUB":
        destination.value = int(n1.value) - int(n2.value)
    elif op=="MUL":
        destination.value = int(n1.value) * int(n2.value)
    elif op=="IDIV":
        if n2.value == 0:
            err_exit(57)
        destination.value = int(n1.value) // int(n2.value)

    destination.type = "int"

def ADD_func(pars):
    MATH_func(pars, "ADD")

def SUB_func(pars):
    MATH_func(pars, "SUB")

def MUL_func(pars):
    MATH_func(pars, "MUL")

def IDIV_func(pars):
    MATH_func(pars, "IDIV")

def COMPARE_func(pars, op):
    destination, symb1, symb2 = pars
    destination = get_variable(destination)
    destination.type = "bool"

    if (symb1[1] == "nil" or symb2[1] == "nil") and op != "EQ":
        err_exit(53)
    elif (symb1[1] == "nil" or symb2[1] == "nil") and op == "EQ":
        if symb1[1] == symb2[1]:
            destination.value = "true"
        else:
            destination.value = "false"
    else:
        compare_types(ConstantClass(symb1[1], symb1[2]), ConstantClass(symb2[1], symb2[2]))
        if op == "EQ":
            destination.value = str(symb1[2] == symb2[2]).lower()
        elif op == "GT":
            destination.value = str(symb1[2] > symb2[2]).lower()
        elif op == "LT":
            destination.value = str(symb1[2] < symb2[2]).lower()

def LT_func(pars):
    COMPARE_func(pars, "LT")

def GT_func(pars):
    COMPARE_func(pars, "GT")

def EQ_func(pars):
    COMPARE_func(pars, "EQ")

def convert_stringbool_to_bool(string):
    if string.value.lower() == "true":
        string.value = True
    elif string.value.lower() == "false":
        string.value = False
    else:
        err_exit(57)

def LOGICAL_COMPARE_func(pars, op):
    var, symb1, symb2 = pars

    var = get_variable(var)
    symb1 = check_if_symb(symb1, "bool")
    symb2 = check_if_symb(symb2, "bool")
    convert_stringbool_to_bool(symb1)
    convert_stringbool_to_bool(symb2)
    var.type="bool"
    if op == "AND":
        var.value = str(symb1.value and symb2.value).lower()
    if op == "OR":
        var.value = str(symb1.value or symb2.value).lower()

def AND_func(pars):
    LOGICAL_COMPARE_func(pars, "AND")

def OR_func(pars):
    LOGICAL_COMPARE_func(pars, "OR")

def NOT_func(pars):
    var, symb1 = pars
    var = get_variable(var)
    symb1 = check_if_symb(symb1, "bool")
    convert_stringbool_to_bool(symb1)
    var.type = "bool"
    var.value = not symb1.value

def INT2CHAR_func(pars):
    var, symb = pars
    var = get_variable(var)
    symb = check_if_symb(symb, "int")
    if int(symb) < 0 or int(symb) > int(1114111):
        err_exit(58)
    var.value = chr(int(symb))
    var.type = "string"

def STRI2INT_func(pars):
    var, symb1, symb2 = pars
    var = get_variable(var)
    symb1 = check_if_symb(symb1, "string")
    symb2 = check_if_symb(symb2, "int")
    if int(symb2.value) >= len(symb1.value):
        err_exit(58)
    var.value = ord(symb1.value[int(symb2.value)])
    var.type = "int"

def READ_func(pars):
    ... #TODO
def WRITE_func(pars):
    ... #TODO

def CONCAT_func(pars):
    var, symb1, symb2 = pars
    var = get_variable(var)
    symb1 = check_if_symb(symb1, "string")
    symb2 = check_if_symb(symb2, "string")
    var.value = str(symb1.value) + str(symb2.value)
    var.type = "string"

def STRLEN_func(pars):
    var, symb = pars
    var = get_variable(var)
    symb = check_if_symb(symb, "string")
    var.value = len(symb.value)
    var.type = "int"

def GETCHAR_func(pars):
    var, symb1, symb2 = pars
    var = get_variable(var)
    symb1 = check_if_symb(symb1, "int")
    symb2 = check_if_symb(symb2, "string")
    if int(symb1.value) < 0 or int(symb1.value) >= len(symb2.value):
        err_exit(58)
    var.value = symb2.value[int(symb1.value)]
    var.type = "string"

def SETCHAR_func(pars):
    var, symb1, symb2 = pars
    var = get_variable(var)
    if var.type != "string":
        err_exit(53)
    symb1 = check_if_symb(symb1, "int")
    symb2 = check_if_symb(symb2, "string")
    if int(symb1.value) < 0 or int(symb1.value) >= len(symb1) or len(symb2.value) == 0:
        err_exit(58)
    var[int(symb1.value)] = symb2[0]

def TYPE_func(pars):
    var, symb = pars
    var = get_variable(var)
    symb = check_if_symb(symb, ".+")
    if symb.type is None:
        var.value = ''
    else:
        var.value = symb.type
    var.type = "string"

def LABEL_func(pars):
    ...#TODO
def JUMP_func(pars):
    ...#TODO
def JUMPIF_func(pars):
    ...#TODO

def EXIT_func(pars):
    symb = pars[0]
    symb = check_if_symb(symb, "int")
    if int(symb.value) < 0 or int(symb.value) > 49:
        err_exit(57)
    exit(int(symb.value))

def DPRINT_func(pars):
    symb = pars[0]
    symb = check_if_symb(symb)
    print(symb.value ,file=stderr)

def BREAK_func():
    print(frames ,file=stderr)


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
    "ADD" : (ADD_func,3),
    "SUB" : (SUB_func,3),
    "MUL" : (MUL_func,3),
    "IDIV" : (IDIV_func,3),
    "LT" : (LT_func,3),
    "GT" : (GT_func,3),
    "EQ" : (EQ_func,3),
    "AND" : (AND_func,3),
    "OR" :  (OR_func,3),
    "NOT" : (NOT_func,2),
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

def interpret_code():
    for i in sorted(instruction_list):
        if not instruction_list[i][1] in instruction_Dictionary:
            err_exit(32)
        check_n_of_args(instruction_Dictionary[instruction_list[i][1]][1], len(instruction_list[i])-2)
        if not len(instruction_list[i])-2:
            instruction_Dictionary[instruction_list[i][1]][0]()
        else:
            instruction_Dictionary[instruction_list[i][1]][0](sorted(instruction_list[i][2:]))

vars = []

def check_code():
    for i in sorted(instruction_list):
        if not instruction_list[i][1] in instruction_Dictionary:
            err_exit(32)
        if instruction_list[i][1] == "LABEL":
            labels.append(i)
        if instruction_list[i][1] == "DEFVAR":
            vars.append(i)

interpret_code()
print(frames)
print(data_stack)

exit(0)
