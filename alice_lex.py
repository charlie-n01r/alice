import ply.lex as lex

reserved_words = {
    'begin'     : 'BEGIN',
    'main'      : 'MAIN',
    'let'       : 'LET',
    'input'     : 'INPUT',
    'print'     : 'PRINT',
    'if'        : 'IF',
    'then'      : 'THEN',
    'else'      : 'ELSE',
    'do'        : 'DO',
    'while'     : 'WHILE',
    'for'       : 'FOR',
    'module'    : 'MODULE',
    'return'    : 'RETURN',
    'endprog'   : 'ENDPROG',
    'end'       : 'END',
    'and'       : 'AND',
    'or'        : 'OR',
    'int'       : 'INT',
    'float'     : 'FLOAT',
    'string'    : 'STRING',
    'void'      : 'VOID',
    'size'      : 'SIZE',
    'mean'      : 'MEAN',
    'median'    : 'MEDIAN',
    'mode'      : 'MODE',
    'variance'  : 'VARIANCE',
    'std'       : 'STD',
    'range'     : 'RANGE',
    'sum'       : 'SUM',
    'min'       : 'MIN',
    'max'       : 'MAX',
    'histogram' : 'HIST',
    'violin'    : 'VIOLIN',
    'box'       : 'BOXPLOT',
    'bar'       : 'BAR',
    'scatter'   : 'SCATTER',
    'mirror'    : 'MIRROR'
}

tokens = [
    'ID',
    'CTE_I',
    'CTE_F',
    'CTE_STRING',
    'EXPONENT',
    'ADD',
    'DECREASE',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQ',
    'NE',
    'ASSIGN',
    'COLON',
    'SEMICOLON',
    'TYPE_ASSIGN',
    'COMA',
    'LPAREN',
    'RPAREN',
    'L_SBRKT',
    'R_SBRKT'
] + list(reserved_words.values())

t_EXPONENT      = r'\^'
t_ADD           = r'\+\+'
t_DECREASE      = r'--'
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_MULTIPLY      = r'\*'
t_DIVIDE        = r'/'
t_ASSIGN         = r'\<-'
t_LE            = r'\<='
t_LT            = r'\<'
t_GE            = r'>='
t_GT            = r'>'
t_EQ            = r'\=\='
t_NE            = r'¬\='
t_TYPE_ASSIGN   = r'\:\:'
t_COLON         = r'\:'
t_SEMICOLON     = r'\;'
t_COMA          = r'\,'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_L_SBRKT       = r'\['
t_R_SBRKT       = r'\]'

t_ignore = ' \t\n\r\f'


def t_ID(t):
    r'[a-zA-Z_]\w*'
    if t.value in reserved_words.keys():
        t.type = reserved_words[t.value]
    else:
        t.type = 'ID'
    return t

def t_CTE_F(t):
    r'\d+\.(\d*)?(e(\+|-)?\d+)?'
    t.value = float(t.value)
    return t

def t_CTE_I(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'"([^\\"\n]+|\\.)*"'
    t.type = 'CTE_STRING'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
