# int, float, string, bool
#   0,     1,      2     3

# row:
# [with int, with float, with string, with bool]

Cube = {
    '++'  : [0, 1, False, False],
    '--'  : [0, 1, False, False],
            #op1 is int           #op1 is float         #op1 is string                #op1 is bool
    '^'   : [[0, 1, False, False], [1, 1, False, False], [False, False, False, False], [False, False, False, False]],
    '*'   : [[0, 1, False, False], [1, 1, False, False], [False, False, False, False], [False, False, False, False]],
    '/'   : [[0, 1, False, False], [1, 1, False, False], [False, False, False, False], [False, False, False, False]],
    '*'   : [[0, 1, False, False], [1, 1, False, False], [False, False, False, False], [False, False, False, False]],
    '+'   : [[0, 1, False, False], [1, 1, False, False], [False, False, False, False], [False, False, False, False]],
    '-'   : [[0, 1, False, False], [1, 1, False, False], [False, False, False, False], [False, False, False, False]],
    '<'   : [[3, 3, False, False], [3, 3, False, False], [False, False, False, False], [False, False, False, False]],
    '<='  : [[3, 3, False, False], [3, 3, False, False], [False, False, False, False], [False, False, False, False]],
    '>'   : [[3, 3, False, False], [3, 3, False, False], [False, False, False, False], [False, False, False, False]],
    '>='  : [[3, 3, False, False], [3, 3, False, False], [False, False, False, False], [False, False, False, False]],
    '=='  : [[3, 3, False, False], [3, 3, False, False], [False, False, 3, False], [False, False, False, 3]],
    '¬='  : [[3, 3, False, False], [3, 3, False, False], [False, False, 3, False], [False, False, False, 3]],
    'and' : [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, 3]],
    'or'  : [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, 3]],
    '<-'  : [[0, False, False, False], [False, 1, False, False], [False, False, 2, False], [False, False, False, 3]]
}

def get_result(coordinates):
    if len(coordinates) == 2:
        opr, op = coordinates
        result = Cube[opr][op]
    else:
        opr, op1, op2 = coordinates
        result = Cube[opr][op1][op2]
    return result
