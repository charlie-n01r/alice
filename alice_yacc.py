import ply.yacc as yacc

from collections.abc import Iterable
from alice_lex import tokens
from sem_cube import get_result
from structs import *

#--------------------------Environment Setup------------------------------------
tmpvar_n = -1
quad_count = -1

S = stacks()
funDir = fun_dir()
constants = cte_table()
variables = var_table()
quadruples = quadruple_list()

memory = memory()
memory.clear()
env = 'global'

#--------------------------Auxiliary Functions----------------------------------
def find(ID, list_name):
    if list_name == 'dec':
        if not variables.var_list:
            return False
        for var in variables.var_list:
            if var.ID != ID:
                continue
            else:
                if env == 'local' and (var.v_address >= 5000 and var.v_address < 10000):
                    return var
                elif env == 'global' and (var.v_address >= 0 and var.v_address < 5000):
                    return var
        return False

    elif list_name == 'cte':
        if not constants.cte_list:
            return False
        for constant in constants.cte_list:
            if constant.ID == ID:
                return constant
        return False

    elif list_name == 'var':
        if not variables.var_list:
            return False
        var_list = variables.var_list.copy()
        var_list.reverse()
        for var in var_list:
            if var.ID != ID:
                continue
            else:
                return var
        return False

def quad_gen(quad):
    global quad_count
    new_quad = quadruple(*quad)
    quadruples.append(new_quad)
    quad_count += 1

def constant_handler(p, cte):
    S.Symbols.append(p[-1])
    S.Types.append(cte)
    if find(p[-1], 'cte') != False:
        return
    else:
        if cte[0] == 0:
            address = memory.ctei[0] + memory.ctei[1]
            memory.ctei[1] += 1
        elif cte[0] == 1:
            address = memory.ctef[0] + memory.ctef[1]
            memory.ctef[1] += 1
        else:
            address = memory.ctes[0] + memory.ctes[1]
            memory.ctes[1] += 1

        new_cte = cte_object(p[-1], address)
        constants.append(new_cte)

def expression_handler(p, operator):
    length = len(S.Operators)
    try:
        size = length - 1 - S.Operators.index('(')
    except ValueError:
        size = length

    if size > 0 and S.Operators[length - 1] == operator:
        temp_der, type_der = (S.Symbols.pop(), S.Types.pop())
        temp_izq, type_izq = (S.Symbols.pop(), S.Types.pop())
        operator = S.Operators.pop()

        res = get_result((operator, type_izq[0], type_der[0]))
        if res is False:
            if operator == 'and' or operator == 'or':
                print(f'Semantic error! Expected two bool operands, got {type_izq[1]} and {type_der[1]}!')
            elif operator in ['==', '¬=', '<', '<=', '>', '>=']:
                print(f'Semantic error! Cannot compare {type_izq[1]} and {type_der[1]}!')
            else:
                print(f'Semantic error! Cannot perform arithmetic operations between {type_izq[1]} and {type_der[1]}!')
            quit()

        global tmpvar_n
        tmpvar_n += 1
        S.Symbols.append('t' + str(tmpvar_n))
        if res == 0:
            restxt = 'int'
        elif res == 1:
            restxt = 'float'
        elif res == 2:
            restxt = 'string'
        else:
            restxt = 'bool'
        S.Types.append((res, restxt))
        quad_gen((operator, temp_izq, temp_der, S.Symbols[len(S.Symbols) - 1]))

def unary_handler(p, operator):
    length = len(S.Operators)
    try:
        size = length - 1 - S.Operators.index('(')
    except ValueError:
        size = length

    if size > 0 and S.Operators[length - 1] == operator:
        temp_der, type_der = (S.Symbols.pop(), S.Types.pop())
        operator = S.Operators.pop()

        if operator == '-':
            if type_der[0] > 1:
                print(f'Semantic error! {type_der[1]} data cannot be turned negative!')
                quit()
            else:
                res = type_der[0]
        else:
            res = get_result((operator, type_der[0]))
            if res is False:
                print(f'Semantic error! Cannot perform arithmetic increment or decrease on {type_der[1]}!')
                quit()

        global tmpvar_n
        tmpvar_n += 1
        S.Symbols.append('t' + str(tmpvar_n))
        if res == 0:
            restxt = 'int'
        elif res == 1:
            restxt = 'float'
        elif res == 2:
            restxt = 'string'
        else:
            restxt = 'bool'
        S.Types.append((res, restxt))
        temp_izq = 0 if operator == '-' else None
        quad_gen((operator, temp_izq, temp_der, S.Symbols[len(S.Symbols) - 1]))

def get_IDs(IDList):
     for item in IDList:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in get_IDs(item):
                 yield x
         else:
             yield item

def export():
    with open('log.txt', 'w') as file:
        file.write(f'Final Status:\nOperands: {S.Symbols}\nTypes: {S.Types}\nLargos: {(len(S.Symbols), len(S.Types))}\nOperators: {S.Operators}\nVariables: {variables.var_list}\nLiterals: {constants.cte_list}\nQuad Count:{quad_count + 1}')
    quadruples.export()
#---------------------------Program Structure-----------------------------------
def p_program(p):
    '''
    program : BEGIN ID COLON global ENDPROG
    '''
    export()

def p_global(p):
    '''
    global : module global
           | declaration global
           | main
    '''

def p_main(p):
    '''
    main : MAIN lclenv_setup stmtblock lclenv_end
    '''

def p_stmtblock(p):
    '''
    stmtblock : COLON initstmt END
    '''

def p_typed_block(p):
    '''
    typed_block : COLON tblck END
    '''

def p_tblck(p):
    '''
    tblck : tblck return
          | initstmt
    '''

def p_initstmt(p):
    '''
    initstmt : stmt stmtchain
             | empty
    '''

def p_stmtchain(p):
    '''
    stmtchain : stmtchain stmt
              | empty
    '''

def p_stmt(p):
    '''
    stmt : assignment
         | conditional
         | print
         | input
         | iteration
         | declaration
         | expression popexpr
    '''

#--------------------------Complex Statements-----------------------------------
def p_conditional(p):
    '''
    conditional : IF expr neuralgic_if THEN stmtblock neuralgic_cond
                | IF expr neuralgic_if THEN COLON initstmt ELSE neuralgic_else stmtblock neuralgic_cond
    '''

def p_iteration(p):
    '''
    iteration : while
              | do_while
              | for
    '''

def p_while(p):
    '''
    while : WHILE neuralgic_while expr while_expr stmtblock while_end
    '''

def p_do_while(p):
    '''
    do_while : DO neuralgic_dw stmtblock WHILE expression dw_end
    '''

def p_for(p):
    '''
    for : FOR ID for_id ASSIGN expr for_expr COLON expr neuralgic_for stmtblock for_end
    '''

#-------------------------------Module------------------------------------------
def p_module(p):
    '''
    module : void_module
           | typed_module
    '''
    p[0] = p[1]

def p_typed_module(p):
    '''
    typed_module : MODULE ID TYPE_ASSIGN type LPAREN params RPAREN typed_block
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]

def p_void_module(p):
    '''
    void_module : MODULE ID TYPE_ASSIGN VOID LPAREN params RPAREN stmtblock
    '''
    p[0] = p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]

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

#-----------------------------Variables-----------------------------------------
def p_assignment(p):
    '''
    assignment : variable ASSIGN expression neuralgic_assign
    '''

def p_declaration(p):
    '''
    declaration : LET ID others TYPE_ASSIGN type idxsize neuralgic_dec SEMICOLON
    '''

def p_others(p):
    '''
    others : others COMA ID
           | empty
    '''
    if len(p) > 2:
        if p[1] == None:
            p[0] = p[3]
        p[0] = p[1], p[3]
    else:
        p[0] = p[1]

def p_idxsize(p):
    '''
    idxsize : L_SBRKT CTE_I R_SBRKT
            | empty
    '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]

#------------------------------Expressions--------------------------------------
def p_expression(p):
    '''
    expression : expr SEMICOLON
    '''

def p_expr(p):
    '''
    expr : andexpr
         | expr OR neuralgic_opr andexpr neuralgic_expr
    '''
    if len(p) <= 2:
        p[0] = p[1]

def p_andexpr(p):
    '''
    andexpr : eqlexpr
            | andexpr AND neuralgic_opr eqlexpr neuralgic_expr
    '''
    if len(p) <= 2:
        p[0] = p[1]

def p_eqlexpr(p):
    '''
    eqlexpr : relexpr
            | eqlexpr eqop neuralgic_opr relexpr neuralgic_expr
    '''
    if len(p) <= 2:
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
            | relexpr relop neuralgic_opr sumexpr neuralgic_expr
    '''
    if len(p) <= 2:
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
            | sumexpr sumop neuralgic_opr term neuralgic_expr
    '''
    if len(p) <= 2:
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
         | term mulop neuralgic_opr unary neuralgic_expr
    '''
    if len(p) <= 2:
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
          | MINUS neuralgic_opr postfix neuralgic_unary
    '''
    if len(p) <= 2:
        p[0] = p[1]

def p_postfix(p):
    '''
    postfix : factor
            | factor postop neuralgic_opr neuralgic_unary
    '''
    p[0] = p[1]

def p_postop(p):
    '''
    postop : ADD
           | DECREASE
    '''
    p[0] = p[1]

def p_factor(p):
    '''
    factor : LPAREN neuralgic_opr expr RPAREN neuralgic_paren
           | value
           | variable neuralgic_var
           | systemdef
           | call
    '''
    if len(p) == 4:
        p[0] = p[3]
    else:
        p[0] = p[1]

def p_value(p):
    '''
    value : CTE_I neuralgic_int
          | CTE_F neuralgic_float
          | CTE_STRING neuralgic_str
    '''
    p[0] = p[1]

def p_variable(p):
    '''
    variable : ID
             | ID L_SBRKT expr R_SBRKT
    '''
    if len(p) > 3:
        p[0] = p[1], p[2], p[3], p[4]
    else:
        p[0] = p[1]

#----------------------------System Functions-----------------------------------
def p_print(p):
    '''
    print : PRINT LPAREN funparam RPAREN neuralgic_print SEMICOLON
    '''

def p_funparam(p):
    '''
    funparam : expr auxparams
             | empty
    '''
    if len(p) > 2:
        if p[2] == None:
            p[0] = p[1]
        p[0] = p[1], p[2]
    else:
        p[0] = p[1]

def p_auxparams(p):
    '''
    auxparams : auxparams COMA expr
              | empty
    '''
    if len(p) > 2:
        if p[1] == None:
            p[0] = p[3]
        p[0] = p[1], p[3]
    else:
        p[0] = p[1]

def p_input(p):
    '''
    input : INPUT LPAREN expr COMA ID RPAREN neuralgic_input SEMICOLON
    '''

def p_systemdef(p):
    '''
    systemdef : SIZE LPAREN ID RPAREN
              | MEAN LPAREN ID RPAREN
              | MEDIAN LPAREN ID RPAREN
              | MODE LPAREN ID RPAREN
              | VARIANCE LPAREN ID RPAREN
              | STD LPAREN ID RPAREN
              | RANGE LPAREN ID RPAREN
    '''
    p[0] = p[1], p[2], p[3], p[4]

def p_call(p):
    '''
    call : ID LPAREN funparam RPAREN
    '''
    p[0] = p[1], p[2], p[3], p[4]

#-------------------------------Typed Rules-------------------------------------
def p_return(p):
    '''
    return : RETURN expression
    '''
    p[0] = p[1], p[2]

def p_type(p):
    '''
    type : INT
         | FLOAT
         | STRING
    '''
    p[0] = p[1]

#---------------------------Neuralgic Rules-------------------------------------
def p_lclenv_setup(p):
    '''
    lclenv_setup :
    '''
    global env
    env = 'local'

def p_lclenv_end(p):
    '''
    lclenv_end :
    '''
    global env
    env = 'global'

def p_popexpr(p):
    '''
    popexpr :
    '''
    S.Symbols.pop()
    S.Types.pop()

def p_neuralgic_assign(p):
    '''
    neuralgic_assign :
    '''
    var = find(p[-3], 'var')
    if not var:
        print(f"Error! Variable '{p[-3]}' doesn't exist!")
        quit()
    else:
        temp_izq, type_izq = (var.ID, var.type)
        temp_der, type_der = (S.Symbols.pop(), S.Types.pop())

        res = get_result((p[-2], type_izq[0], type_der[0]))
        if res is False:
            print(f'Semantic error! Type mismatch! Got {type_izq[1]} and {type_der[1]}!')
            quit()

        quad_gen((p[-2], None, temp_der, var.ID))

def p_neuralgic_dec(p):
    '''
    neuralgic_dec :
    '''
    if p[-4] == None:
        IDList = [p[-5]]
    else:
        IDList = list(get_IDs(p[-4]))
        IDList.insert(0, p[-5])
    for ID in IDList:
        if ID == None:
            continue
        if find(ID, 'dec') != False:
            print(f"Error! Variable '{ID}' already declared!")
            quit()

        if p[-2] == 'int':
            type = (0, p[-2])
            if env == 'global':
                address = memory.gbli[0] + memory.gbli[1]
                if address >= memory.gblf[0]:
                    print(f'Error! Too many global integer variables!')
                    quit()
                memory.gbli[1] += 1
            else:
                address = memory.lcli[0] + memory.lcli[1]
                if address >= memory.lclf[0]:
                    print(f'Error! Too many local integer variables!')
                    quit()
                memory.lcli[1] += 1

        elif p[-2] == 'float':
            type = (1, p[-2])
            if env == 'global':
                address = memory.gblf[0] + memory.gblf[1]
                if address >= memory.gbls[0]:
                    print(f'Error! Too many global float variables!')
                    quit()
                memory.gblf[1] += 1
            else:
                address = memory.lclf[0] + memory.lclf[1]
                if address >= memory.lcls[0]:
                    print(f'Error! Too many local float variables!')
                    quit()
                memory.lclf[1] += 1

        else:
            type = (2, p[-2])
            if env == 'global':
                address = memory.gbls[0] + memory.gbls[1]
                if address >= memory.lcli[0]:
                    print(f'Error! Too many global string variables!')
                    quit()
                memory.gbls[1] += 1
            else:
                address = memory.lcls[0] + memory.lcls[1]
                if address >= memory.tmpi[0]:
                    print(f'Error! Too many local string variables!')
                    quit()
                memory.lcls[1] += 1

        if p[-1] == None:
            arr_size = 1
        else:
            arr_size = int(p[-1])
        new_var = var_object(ID, type, address, arr_size)
        variables.append(new_var)

def p_neuralgic_opr(p):
    '''
    neuralgic_opr :
    '''
    S.Operators.append(p[-1])

def p_neuralgic_int(p):
    '''
    neuralgic_int :
    '''
    constant_handler(p, (0, 'int'))

def p_neuralgic_float(p):
    '''
    neuralgic_float :
    '''
    constant_handler(p, (1, 'float'))

def p_neuralgic_str(p):
    '''
    neuralgic_str :
    '''
    constant_handler(p, (2, 'string'))

def p_neuralgic_var(p):
    '''
    neuralgic_var :
    '''
    var = find(p[-1], 'var')
    if not var:
        print(f"Error! Variable '{p[-1]}' doesn't exist!")
        quit()

    S.Symbols.append(p[-1])
    S.Types.append(var.type)

def p_neuralgic_paren(p):
    '''
    neuralgic_paren :
    '''
    S.Operators.pop()

def p_neuralgic_expr(p):
    '''
    neuralgic_expr :
    '''
    expression_handler(p, p[-3])

def p_neuralgic_unary(p):
    '''
    neuralgic_unary :
    '''
    if p[-2] == '++' or p[-2] == '--':
        unary_handler(p, p[-2])
    else:
        unary_handler(p, p[-3])

def p_neuralgic_print(p):
    '''
    neuralgic_print :
    '''
    global quad_count
    if p[-2] == None:
        quad_gen(('Print', None, None, r'\n'))
    else:
        temp_quads = quadruple_list()
        IDList = list(get_IDs(p[-2]))
        for i in range(len(IDList)):
            if IDList[i] == None:
                continue
            res = res = find(IDList[i], 'cte')
            if not res:
                res= find(IDList[i], 'var')
                if not res:
                    print(f"Error! Variable '{IDList[i]}' doesn't exist!")
                    quit()

            msg = S.Symbols.pop()
            S.Types.pop()
            if i == 0:
                new_quad = quadruple('Print', None, None, str(msg) + r'\n')
            else:
                new_quad = quadruple('Print', None, None, str(msg) + ' ')
            temp_quads.append(new_quad)

        temp_quads.quadruples = list(reversed(temp_quads.quadruples))
        for quad in temp_quads.quadruples:
            quadruples.append(quad)
            quad_count += 1

def p_neuralgic_input(p):
    '''
    neuralgic_input :
    '''
    res = find(p[-4], 'cte')
    if not res:
        res= find(p[-4], 'var')
        if not res:
            print(f"Error! Variable '{p[-4]}' doesn't exist!")
            quit()

    msg = S.Symbols.pop()
    mtype = S.Types.pop()
    if mtype[0] != 2:
        print(f"Error while performing input! '{p[-4]}' is not a string!")
        quit()
    storage = find(p[-2], 'var')
    if not storage:
        print(f"Error! Variable '{p[-2]}' doesn't exist!")
        quit()

    quad_gen(('Print', None, None, msg))
    quad_gen(('Input', None, None, storage.ID))

def p_neuralgic_if(p):
    '''
    neuralgic_if :
    '''
    expr_type = S.Types.pop()
    if expr_type[0] != 3:
        print(f'Error! Cannot evaluate the truth value of {expr_type[1]} expressions!')
        quit()
    res = S.Symbols.pop()

    quad_gen(('GotoF', res, None, None))
    S.Jumps.append(quad_count)

def p_neuralgic_cond(p):
    '''
    neuralgic_cond :
    '''
    end = S.Jumps.pop()
    quadruples.quadruples[end].storage = quad_count + 1

def p_neuralgic_else(p):
    '''
    neuralgic_else :
    '''
    quad_gen(('Goto', None, None, None))

    false = S.Jumps.pop()
    S.Jumps.append(quad_count)

    quadruples.quadruples[false].storage = quad_count + 1

def p_neuralgic_while(p):
    '''
    neuralgic_while :
    '''
    S.Jumps.append(quad_count + 1)

def p_while_expr(p):
    '''
    while_expr :
    '''
    expr_type = S.Types.pop()
    if expr_type[0] != 3:
        print(f'Error! Cannot evaluate the truth value of {expr_type[1]} expressions!')
        quit()
    res = S.Symbols.pop()

    quad_gen(('GotoF', res, None, None))
    S.Jumps.append(quad_count)

def p_while_end(p):
    '''
    while_end :
    '''
    end = S.Jumps.pop()
    goback = S.Jumps.pop()

    quad_gen(('Goto', None, None, goback))
    quadruples.quadruples[end].storage = quad_count + 1

def p_neuralgic_dw(p):
    '''
    neuralgic_dw :
    '''
    S.Jumps.append(quad_count + 1)

def p_dw_end(p):
    '''
    dw_end :
    '''
    expr_type = S.Types.pop()
    if expr_type[0] != 3:
        print(f'Error! Cannot evaluate the truth value of {expr_type[1]} expressions!')
        quit()
    res = S.Symbols.pop()
    goback = S.Jumps.pop()
    quad_gen(('GotoT', res, None, goback))

def p_for_id(p):
    '''
    for_id :
    '''
    var = find(p[-1], 'var')
    if not var:
        print(f"Error! Variable '{p[-1]}' not found!")
        quit()
    if var.type[0] > 0:
        print(f"Semantic error! Type mismatch! Expected int, got {var.type[1]}!")
        quit()

    S.Symbols.append(var.ID)
    S.Types.append(var.type)

def p_for_expr(p):
    '''
    for_expr :
    '''
    expr_type = S.Types.pop()
    if expr_type[0] > 0:
        print(f"Semantic error! Type mismatch! Expected int, got {expr_type[1]}!")
        quit()
    expr = S.Symbols.pop()

    global control
    control = S.Symbols[len(S.Symbols) - 1]
    control_type = S.Types[len(S.Types) - 1]

    res = get_result((p[-2], control_type[0], expr_type[0]))
    if res is False:
        print(f'Semantic error! Type mismatch! Got {type_izq[1]} and {type_der[1]}!')
        quit()

    quad_gen((p[-2], None, expr, control))

def p_neuralgic_for(p):
    '''
    neuralgic_for :
    '''
    expr_type = S.Types.pop()
    if expr_type[0] > 0:
        print(f"Semantic error! Type mismatch! Expected int, got {expr_type[1]}!")
        quit()
    expr = S.Symbols.pop()
    control = S.Symbols[len(S.Symbols) - 1]

    global tmpvar_n
    global quad_count
    tmpvar_n += 1
    tn = 't' + str(tmpvar_n)
    quad_gen(('<-', control, None, 'vcontrol'))
    quad_gen(('<-', expr, None, 'vfinal'))
    quad_gen(('<', 'vcontrol', 'vfinal', tn))

    tn = 't' + str(tmpvar_n)
    S.Jumps.append(quad_count)
    quad_gen(('GotoF', tn, None, None))
    S.Jumps.append(quad_count)

def p_for_end(p):
    '''
    for_end :
    '''
    global tmpvar_n
    tmpvar_n += 1
    tn = 't' + str(tmpvar_n)

    quad_gen(('+', 'vcontrol', 1, tn))
    quad_gen(('<-', tn, None, 'vcontrol'))
    quad_gen(('<-', tn, 1, S.Symbols[len(S.Symbols) - 1]))

    end = S.Jumps.pop()
    goback = S.Jumps.pop()
    quad_gen(('Goto', None, None, goback))
    quadruples.quadruples[end].storage = quad_count + 1
    S.Symbols.pop()
    S.Types.pop()

#------------------------------Aux Rules----------------------------------------
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(t):
    if t is not None:
        print("Line %s, illegal token: %s" % (t.lineno, t.value))
    else:
        print('Unexpected end of input')
    quit()

parser = yacc.yacc()
