import json

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

class fun_object:
    def __init__(self, ID, type):
        self.ID = ID
        self.type = type
        self.scope = scope
        self.parameters = []
        self.variables = []

class fun_dir:
    def __init__(self):
        self.fun_list = []

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

    def export(self):
        export_list = []
        for quadruple in self.quadruples:
            quad = [quadruple.operation, quadruple.operand1, quadruple.operand2, quadruple.storage]
            export_list.append(quad)

        with open('quadruples.json', 'w', encoding='utf-8') as file:
            json.dump(export_list, file, ensure_ascii=False, indent=4)

class stacks:
    def __init__(self):
        self.Operators = []
        self.Symbols = []
        self.Types = []
        self.Jumps = []

class memory:
    def __init__(self):
        self.gbli = [0, 0]
        self.gblf = [2000, 0]
        self.gbls = [4000, 0]

        self.lcli = [5000, 0]
        self.lclf = [7000, 0]
        self.lcls = [9000, 0]

        self.tmpi = [10000, 0]
        self.tmpf = [15000, 0]
        self.tmpb = [20000, 0]

        self.ctei = [25000, 0]
        self.ctef = [27000, 0]
        self.ctes = [29000, 0]

    def clear(self):
        self.gbli[1] = 0
        self.gblf[1] = 0
        self.gbls[1] = 0

        self.lcli[1] = 0
        self.lclf[1] = 0
        self.lcls[1] = 0

        self.tmpi[1] = 0
        self.tmpf[1] = 0
        self.tmpb[1] = 0

        self.ctei[1] = 0
        self.ctef[1] = 0
        self.ctes[1] = 0
