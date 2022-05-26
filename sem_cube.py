# int, float, string, bool pointer
#   0      1       2     3       4

# row:
# [with int, with float, with string, with bool]

Cube = {
    '++'  : [0, 1, False, False, 4],
    '--'  : [0, 1, False, False, 4],
            #op1 is int               #op1 is float            #op1 is string                   #op1 is bool                     #op1 is pointer
    '^'   : [[0, 1, False, False, 4], [1, 1, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '*'   : [[0, 1, False, False, 4], [1, 1, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '/'   : [[1, 1, False, False, 4], [1, 1, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '*'   : [[0, 1, False, False, 4], [1, 1, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '+'   : [[0, 1, False, False, 4], [1, 1, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '-'   : [[0, 1, False, False, 4], [1, 1, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '<'   : [[3, 3, False, False, 4], [3, 3, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '<='  : [[3, 3, False, False, 4], [3, 3, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '>'   : [[3, 3, False, False, 4], [3, 3, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '>='  : [[3, 3, False, False, 4], [3, 3, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [4, 4, 4, 4, 4]],
    '=='  : [[3, 3, False, False, 4], [3, 3, False, False, 4], [False, False, 3, False, 4], [False, False, False, 3, 4], [4, 4, 4, 4, 4]],
    '¬='  : [[3, 3, False, False, 4], [3, 3, False, False, 4], [False, False, 3, False, 4], [False, False, False, 3, 4], [4, 4, 4, 4, 4]],
    'and' : [[False, False, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [False, False, False, 3, 4], [4, 4, 4, 4, 4]],
    'or'  : [[False, False, False, False, 4], [False, False, False, False, 4], [False, False, False, False, 4], [False, False, False, 3, 4], [4, 4, 4, 4, 4]],
    '<-'  : [[0, False, False, False, 4], [False, 1, False, False, 4], [False, False, 2, False, 4], [False, False, False, 3, 4], [4, 4, 4, 4, 4]]
}

def get_result(coordinates):
    if len(coordinates) == 2:
        opr, op = coordinates
        result = Cube[opr][op]
    else:
        opr, op1, op2 = coordinates
        result = Cube[opr][op1][op2]
    return result
