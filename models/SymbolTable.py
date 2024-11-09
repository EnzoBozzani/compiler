import sys

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare_variable(self, name, var_type):
        if name in self.symbols:
            print(f"ERRO SEMÂNTICO: Variável '{name}' já foi declarada.")
            sys.exit()
        self.symbols[name] = var_type

    def get_variable_type(self, name):
        if name not in self.symbols:
            print(f"ERRO SEMÂNTICO: Variável '{name}' não foi declarada.")
            sys.exit()
        return self.symbols[name]