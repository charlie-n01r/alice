import ply.lex as lex

reserved_words = {
    'program' : 'PROGRAM',
    'var'     : 'VAR',
    'int'     : 'INT',
    'float'   : 'FLOAT',
    'if'      : 'IF',
    'else'    : 'ELSE',
    'print'   : 'PRINT'
}

tokens = [
    'ID',
    'COLON',
    'SEMICOLON',
    'COMA',
    'L_PAREN',
    'R_PAREN',
    'L_CURL',
    'R_CURL',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'ASIGN',
    'LT',
    'GT',
    'DIFF',
    'CTE_STRING',
    'CTE_I',
    'CTE_F'
] + list(reserved_words.values())


t_PROGRAM = r'program'
t_COLON = r'\:'
t_VAR = r'var'
t_SEMICOLON = r'\;'
t_COMA = r'\,'
t_INT = r'int'
t_FLOAT = r'float'
t_IF = r'if'
t_ELSE = r'else'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_CURL = r'\{'
t_R_CURL = r'\}'
t_PRINT = r'print'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_ASIGN = r'\='
t_LT = r'\<'
t_GT = r'>'
t_DIFF = r'\<>'

t_ignore = ' \t\n\r\f'


def t_ID(t):
    r'[a-zA-Z_]\w*'
    if t.value in reserved_words.keys():
        t.type = reserved_words[t.value]
    else:
        t.type = 'ID'
    return t

def t_CTE_F(t):
    r'\d+\.(\d*)?(E(\+|-)?\d+)?'
    t.value = float(t.value)
    return t

def t_CTE_I(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'\"(.|\s)*\"'
    t.type = 'CTE_STRING'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
