import ply.yacc as yacc

from alice_lex import tokens

def p_programa(p):
    '''
    programa : PROGRAM ID COLON v bloque
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5]

def p_v(p):
    '''
    v : vars
      | empty
    '''
    p[0] = p[1]

def p_vars(p):
    '''
    vars : VAR vrs
    '''
    p[0] = p[1], p[2]

def p_vrs(p):
    '''
    vrs : ID others COLON tipo SEMICOLON rvrs
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5], p[6]

def p_vrss(p):
    '''
    rvrs : vrs
         | empty
    '''
    p[0] = p[1]

def p_others(p):
    '''
    others : COMA ID others
           | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2], p[3]

def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
    '''
    p[0] = p[1]

def p_bloque(p):
    '''
    bloque : L_CURL est R_CURL
    '''
    p[0] = p[1], p[2], p[3]

def p_est(p):
    '''
    est : estatuto est
        | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2]

def p_estatuto(p):
    '''
    estatuto : condicion
             | escritura
             | asignacion
    '''
    p[0] = p[1]

def p_asignacion(p):
    '''
    asignacion : ID ASIGN expresion SEMICOLON
    '''
    p[0] = p[1], p[2], p[3], p[4]

def p_expresion(p):
    '''
    expresion : exp e
    '''
    p[0] = p[1], p[2]

def p_e(p):
    '''
    e : GT exp e
      | LT exp e
      | DIFF exp e
      | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2], p[3]

def p_condicion(p):
    '''
    condicion : IF L_PAREN expresion R_PAREN bloque else SEMICOLON
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5], p[6], p[7]

def p_else(p):
    '''
    else : ELSE bloque
         | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2]

def p_escritura(p):
    '''
    escritura : PRINT L_PAREN str scr R_PAREN SEMICOLON
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5], p[6]

def p_scr(p):
    '''
    scr : COMA str scr
        | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2], p[3]

def p_str(p):
    '''
    str : expresion
        | CTE_STRING
    '''
    p[0] = p[1]

def p_exp(p):
    '''
    exp : termino t
    '''
    p[0] = p[1], p[2]

def p_t(p):
    '''
    t : sign1 termino t
      | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2], p[3]

def p_sign1(p):
    '''
    sign1 : PLUS
          | MINUS
    '''
    p[0] = p[1]

def p_termino(p):
    '''
    termino : factor f
    '''
    p[0] = p[1], p[2]

def p_f(p):
    '''
    f : sign2 factor f
      | empty
    '''
    if p[1] == None:
        p[0] = p[1]
    else:
        p[0] = p[1], p[2], p[3]

def p_sign2(p):
    '''
    sign2 : MULTIPLY
          | DIVIDE
    '''
    p[0] = p[1]

def p_factor(p):
    '''
    factor : L_PAREN expresion R_PAREN
           | fsign var_cte
    '''
    if p[1] == '+' or p[1] == '-' or p[1] == None:
        p[0] = p[1], p[2]
    else:
        p[0] = p[1], p[2], p[3]

def p_fsign(p):
    '''
    fsign : sign1
          | empty
    '''
    p[0] = p[1]

def p_var_cte(p):
    '''
    var_cte : ID
            | CTE_I
            | CTE_F
    '''
    p[0] = p[1]

# Empty rule

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Catch errors

def p_error(token):
    if token is not None:
        print("Line %s, illegal token: %s" % (token.lineno, token.value))
    else:
        print('Unexpected end of input')
    quit()

parser = yacc.yacc()

## Read input from user for testing

while True:
    try:
        file_name = input('>Insert file name: ')
        print(file_name)
        test_file = open(file_name)
        source_code = test_file.read()
        test_file.close()
    except (KeyboardInterrupt, EOFError):
        quit('')
    except FileNotFoundError:
        print('Error! Wrong file name!')
        continue
    parser.parse(source_code)
    print(f"Successfully parsed '{file_name}'!!")
