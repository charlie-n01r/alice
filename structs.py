import json

def export(Q, C, D):
    export_dict = {}

    temp = []
    for module in D.modules:
        mdl = [module.ID, module.prototyping, module.size]
        temp.append(mdl)
    export_dict['modules'] = temp

    temp = []
    for constant in C.cte_list:
        cte = [constant.ID, constant.v_address]
        temp.append(cte)
    export_dict['constants'] = temp

    temp = []
    for quadruple in Q.quadruples:
        quad = [quadruple.operation, quadruple.operand1, quadruple.operand2, quadruple.storage]
        temp.append(quad)
    export_dict['code'] = temp

    with open('obj.json', 'w', encoding='utf-8') as file:
        json.dump(export_dict, file, ensure_ascii=False, indent=2)

class var_object:
    def __init__(self, ID, type, v_address, arr_size):
        self.ID = ID
        self.type = type
        self.v_address = v_address
        self.arr_size = arr_size

    def __repr__(self):
        return f'({self.ID}, {self.type[1]}, {self.v_address}, {self.arr_size})'

class var_table:
    def __init__(self):
        self.var_list = []

    def append(self, value):
        self.var_list.append(value)

    def copy(self):
        return self.var_list.copy()

    def __repr__(self):
        return f'{self.var_list}'

class cte_object:
    def __init__(self, ID, v_address):
        self.ID = ID
        self.v_address = v_address

    def __repr__(self):
        return f'({self.ID}, {self.v_address})'

class cte_table:
    def __init__(self):
        self.cte_list = []

    def append(self, value):
        self.cte_list.append(value)

class mdl_object:
    def __init__(self, ID, type, beginning, table, values, size):
        self.ID = ID
        self.type = type
        self.beginning = beginning
        self.variables = table
        self.prototyping = values
        self.size = size

    def __repr__(self):
        return f'({self.ID}, {self.type}, {self.beginning}, {self.variables}, {self.prototyping}, {self.size})'

class mdl_dir:
    def __init__(self):
        self.modules = []

    def append(self, module):
        self.modules.append(module)

class quadruple:
    def __init__(self, operation, operand1, operand2, storage):
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.storage = storage

    def __repr__(self):
        return f'({self.operation}, {self.operand1}, {self.operand2}, {self.storage})'

class quadruple_list:
    def __init__(self):
        self.quadruples = []

    def append(self, quadruple):
        self.quadruples.append(quadruple)

class stacks:
    def __init__(self):
        self.Operators = []
        self.Symbols = []
        self.Types = []
        self.Jumps = []

class memory:
    def __init__(self):
        self.gbli = [1000, 0]
        self.gblf = [3000, 0]
        self.gbls = [5000, 0]

        self.lcli = [6000, 0]
        self.lclf = [8000, 0]
        self.lcls = [10000, 0]

        self.tmpi = [11000, 0]
        self.tmpf = [16000, 0]
        self.tmpb = [21000, 0]

        self.ctei = [26000, 0]
        self.ctef = [27500, 0]
        self.ctes = [29000, 0]

    def clear(self):
        self.lcli[1] = 0
        self.lclf[1] = 0
        self.lcls[1] = 0

        self.tmpi[1] = 0
        self.tmpf[1] = 0
        self.tmpb[1] = 0
