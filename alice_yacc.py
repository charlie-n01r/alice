import ply.yacc as yacc

from alice_lex import tokens

def p_program(p):
    '''
    program : BEGIN ID COLON global ENDPROG
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5]
    print(p[0])

def p_global(p):
    '''
    global : main
           | gdeclr
    '''
    p[0] = p[1]

def p_gdeclr(p):
    '''
    gdeclr : declaration global
           | module global
    '''
    p[0] = p[1], p[2]

def p_main(p):
    '''
    main : MAIN COLON initstmt END
    '''
    p[0] = p[1], p[2], p[3], p[4]

def p_initstmt(p):
    '''
    initstmt : stmt stmtchain
             | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2]
    else:
        p[0] = p[1]

def p_stmtchain(p):
    '''
    stmtchain : stmtchain stmt
              | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2]
    else:
        p[0] = p[1]

def p_stmt(p):
    '''
    stmt : complex
         | simple
    '''
    p[0] = p[1]

def p_simple(p):
    '''
    simple : declaration
           | assignment
           | expression
           | return
    '''
    p[0] = p[1]

def p_declaration(p):
    '''
    declaration : LET ID others TYPE_ASSIGN type idxsize SEMICOLON
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5]

def p_assignment(p):
    '''
    assignment : variable ASSIGN expression
    '''
    p[0] = p[1], p[2], p[3]

def p_others(p):
    '''
    others : others COMA ID
           | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_type(p):
    '''
    type : INT
         | FLOAT
         | STRING
    '''
    p[0] = p[1]

def p_idxsize(p):
    '''
    idxsize : L_SBRKT CTE_I R_SBRKT
            | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_expression(p):
    '''
    expression : expr SEMICOLON
    '''
    p[0] = p[1], p[2]

def p_expr(p):
    '''
    expr : andexpr
         | expr OR andexpr
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_andexpr(p):
    '''
    andexpr : eqlexpr
            | andexpr AND eqlexpr
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_eqlexpr(p):
    '''
    eqlexpr : relexpr
            | eqlexpr eqop relexpr
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_eqop(p):
    '''
    eqop : EQ
         | NE
    '''
    p[0] = p[1]

def p_relexpr(p):
    '''
    relexpr : sumexpr
            | relexpr relop sumexpr
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_relop(p):
    '''
    relop : LE
          | LT
          | GE
          | GT
    '''
    p[0] = p[1]

def p_sumexpr(p):
    '''
    sumexpr : term
            | sumexpr sumop term
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_sumop(p):
    '''
    sumop : PLUS
          | MINUS
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : unary
         | term mulop unary
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_mulop(p):
    '''
    mulop : EXPONENT
          | MULTIPLY
          | DIVIDE
    '''
    p[0] = p[1]

def p_unary(p):
    '''
    unary : postfix
          | sumop postfix
    '''
    if len(p) > 2:
        p[0] = p[1], p[2]
    else:
        p[0] = p[1]

def p_postfix(p):
    '''
    postfix : factor
            | factor postop
    '''
    if len(p) > 2:
        p[0] = p[1], p[2]
    else:
        p[0] = p[1]

def p_postop(p):
    '''
    postop : ADD
           | DECREASE
    '''
    p[0] = p[1]

def p_factor(p):
    '''
    factor : LPAREN expr RPAREN
           | value
           | variable
           | call
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_value(p):
    '''
    value : CTE_I
          | CTE_F
          | CTE_STRING
    '''
    p[0] = p[1]

def p_variable(p):
    '''
    variable : ID
             | ID L_SBRKT expr R_SBRKT
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3], p[4]
    else:
        p[0] = p[1]

def p_call(p):
    '''
    call : userdef
         | systemdef
    '''
    p[0] = p[1]

def p_userdef(p):
    '''
    userdef : ID LPAREN funparam RPAREN
    '''
    p[0] = p[1], p[2], p[3], p[4]

def p_funparam(p):
    '''
    funparam : expr auxparams
             | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2]
    else:
        p[0] = p[1]

def p_auxparams(p):
    '''
    auxparams : auxparams COMA expr
              | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_systemdef(p):
    '''
    systemdef : INPUT LPAREN expr RPAREN
              | PRINT LPAREN expr auxparams RPAREN
              | SIZE LPAREN expr RPAREN
              | MEAN LPAREN expr RPAREN
              | MEDIAN LPAREN expr RPAREN
              | MODE LPAREN expr RPAREN
              | VARIANCE LPAREN expr RPAREN
              | STD LPAREN expr RPAREN
              | RANGE LPAREN expr RPAREN
    '''
    if len(p) < 6:
        p[0] = p[1], p[2], p[3], p[4]
    else:
        p[0] = p[1], p[2], p[3], p[4], p[5]


def p_return(p):
    '''
    return : RETURN expression
    '''
    p[0] = p[1], p[2]

def p_complex(p):
    '''
    complex : conditional
            | iteration
    '''
    p[0] = p[1]

def p_module(p):
    '''
    module : MODULE ID TYPE_ASSIGN funtype LPAREN params RPAREN COLON initstmt END
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]

def p_funtype(p):
    '''
    funtype : VOID
            | type
    '''
    p[0] = p[1]

def p_params(p):
    '''
    params : ID TYPE_ASSIGN type rparams
           | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3], p[4]
    else:
        p[0] = p[1]

def p_rparams(p):
    '''
    rparams : rparams COMA ID TYPE_ASSIGN type
            | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3], p[4], p[5]
    else:
        p[0] = p[1]

def p_conditional(p):
    '''
    conditional : IF expr THEN COLON initstmt else END
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5], p[6], p[7]

def p_else(p):
    '''
    else : ELSE COLON initstmt
         | empty
    '''
    if len(p) > 2:
        p[0] = p[1], p[2], p[3]
    else:
        p[0] = p[1]

def p_iteration(p):
    '''
    iteration : WHILE expr COLON initstmt END
              | DO COLON initstmt COLON WHILE expr END
              | FOR LPAREN assignment expression expression RPAREN COLON initstmt END
    '''
    if len(p) == 6:
        p[0] = p[1], p[2], p[3], p[4], p[5]
    elif len(p) == 8:
        p[0] = p[1], p[2], p[3], p[4], p[5], p[6], p[7]
    else:
        p[0] = p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]

# Empty rule
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Catch errors

def p_error(t):
    if t is not None:
        print("Line %s, illegal token: %s" % (t.lineno, t.value))
    else:
        print('Unexpected end of input')
    quit()

parser = yacc.yacc()
