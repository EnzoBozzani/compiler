import sys

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scopes = [0] 
    
    def enter_scope(self):
        self.scopes.append(self.scopes[-1] + 1)
    
    def exit_scope(self):
        self.scopes.pop()
    
    def declare_variable(self, name, var_type):
        current_scope = self.scopes[-1]
        
        if name in self.symbols:
            if current_scope == self.symbols[name]["scope"][-1]:
                print(f"ERRO SEMÂNTICO: Variável '{name}' já foi declarada no escopo atual.")
                sys.exit()
            else:
                self.symbols[name]["scope"].append(current_scope)
        else:
            self.symbols[name] = { "var_type": var_type, "scope": [current_scope] }
    
    def get_variable_type(self, name):
        if name not in self.symbols:
            print(f"ERRO SEMÂNTICO: Variável '{name}' não foi declarada.")
            sys.exit()

        current_scope = self.scopes[-1]
        for scope in reversed(self.symbols[name]["scope"]):
            if scope <= current_scope:
                return self.symbols[name]["var_type"]
        
        print(f"ERRO SEMÂNTICO: Variável '{name}' não encontrada no escopo atual.")
        sys.exit()
