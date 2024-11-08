class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare_variable(self, name, var_type):
        if name in self.symbols:
            raise Exception(f"Semantic Error: Variable '{name}' already declared.")
        self.symbols[name] = var_type

    def get_variable_type(self, name):
        if name not in self.symbols:
            raise Exception(f"Semantic Error: Variable '{name}' is not declared.")
        return self.symbols[name]