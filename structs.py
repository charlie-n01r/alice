class var_object:
    def __init__(self, ID, type, value, scope, arr_size):
        self.ID = ID
        self.type = type
        self.value = value
        self.scope = scope
        self.arr_size = arr_size

class var_table:
    def __init__(self):
        self.var_list = []

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
    def __init__(self):
        self.operation = None
        self.operand1 = None
        self.operand2 = None
        self.storage = None

    def set_operation(self, operation):
        self.operation = operation

    def set_operand1(self, operand1):
        self.operand1 = operand1

    def set_operand2(self, operand2):
        self.operand2 = operand2

    def set_storage(self, storage):
        self.storage = storage

    def __repr__(self):
        return f'({self.operation}, {self.operand1}, {self.operand2}, {self.storage})'

class stacks:
    def __init__(self):
        self.SOperator = []
        self.SSymbols = []
        self.SGoto = []
