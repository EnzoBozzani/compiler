import sys

from models import Token

class SyntaticAnalysis():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.previous_tokens = []
        self.expecting = 0
        self.previous = None
        self.trees = []
        self.token = self.tokens.pop(0)

        print([t.to_string() for t in self.tokens])

        self.run()

    def run(self):
        first = True
        while len(self.tokens) > 0:
            if first: 
                first = False
            else:
                self.next_token()

            if self.if_statement():
                print(f"Success: if.")
                # TODO: buildar ast
            elif self.attr_expression():
                print(f"Success: attr_expression.")
                # TODO: buildar ast
            elif self.init_expression():
                print(f"Success: init_expression.")
                # TODO: buildar ast
            # TODO:
            else:
                print(f"ERROR: No matching rule for {self.token.to_string()}")
                sys.exit()
            
            if (self.expecting == 0):
                pass
                # TODO: lógica pra sair do self.run

               

    def next_token(self):
        if len(self.tokens) <= 0: return
        if self.previous is not None: self.previous_tokens.insert(0, self.previous)
        self.previous = self.token
        self.token = self.tokens.pop(0)
        if self.token.get_type() == 'open_curly_braces': self.expecting += 1
        if self.token.get_type() == 'close_curly_braces': self.expecting -= 1
        # print(f"TOKEN: {self.token.to_string()}")
    
    def previous_token(self):
        if self.token is not None: self.tokens.insert(0, self.token)
        self.token = self.previous
        self.previous = self.previous_tokens.pop(0) if len(self.previous_tokens) > 0 else None
        if self.token.get_type() == 'open_curly_braces': self.expecting -= 1
        if self.token.get_type() == 'close_curly_braces': self.expecting += 1
    
    def error(self, rule: str):
        self.errors.append(f"Not expected: {self.token}. Rule: {rule}")
    
    def math_e(self):
        if self.math_t():
            self.next_token()
            if self.math_e_():
                return True
            else:
                self.previous_token()
        
    
        return False

    def math_e_(self):
        if self.token.get_type() in ['add', 'sub']:
            self.next_token()
            if self.math_t():
                self.next_token()
                if self.math_e_():
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
        
        self.previous_token()
        return True

    def math_t(self):
        if self.math_f():
            self.next_token()
            if self.math_t_():
                return True
            else:
                self.previous_token()
        
        return False

    def math_t_(self):
        if self.token.get_type() in ['mult', 'div']:
            self.next_token()
            if self.math_f():
                self.next_token()
                if self.math_t_():
                    return True
                else: 
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
        
        self.previous_token()
        return True
    
    def math_f(self):
        if self.token.get_type() == 'op':
            self.next_token()
            if self.math_e():
                self.next_token()
                if self.token.get_type() == 'cp':
                    return True
                else: 
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()

        elif self.math_n():
            return True


        return False
    
    def math_n(self):
        if self.math_d():
            self.next_token()
            if self.math_n_():
                return True
            else:
                self.previous_token()
        
        return False
    
    def math_n_(self):
        if self.math_d():
            self.next_token()
            if self.math_n_():
                return True
            else: 
                self.previous_token()
        
        self.previous_token()
        return True
    
    def math_d(self):
        if self.token.get_type() in ['id', 'number']:
            return True
        
        return False
    
    def value(self):
        if self.token.get_type() in ['number', 'id']:
            self.next_token()
            if self.token.get_type() in ['add', 'sub', 'div', 'mult']:
                self.next_token()
                if self.math_e():
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()

        if self.token.get_type() in ['number', 'id', 'string', 'true', 'false']:
            return True
        elif self.math_e():
            return True
        
        return False

    def condition(self):
        if self.value():
            self.next_token()
            if self.condition_():
                return True
            else:
                self.previous_token()
        
        return False
    
    def condition_(self):
        if self.comparison_operator():
            self.next_token()
            if self.value():
                return True
            else:
                self.previous_token()

        self.previous_token()
        return True
    
    def comparison_operator(self):
        if self.token.get_type() in ['gt', 'equal', 'gte', 'lte', 'lt']:
            return True
        
        return False
    
    def if_statement(self):
        if self.token.get_type() == 'if_reserved':
            self.next_token()
            if self.token.get_type() == 'op':
                self.next_token()
                if self.condition():
                    self.next_token()
                    if self.token.get_type() == 'cp':
                        self.next_token()
                        if self.token.get_type() == 'open_curly_braces':
                            self.next_token()
                            if self.all(self.expecting - 1):
                                self.next_token()
                                if self.token.get_type() == 'close_curly_braces':
                                    self.next_token()
                                    if self.token.get_type() == 'else_reserved':
                                        # TODO: ; lógica do else
                                        pass
                                    else:
                                        if len(self.tokens) > 0: self.previous_token()
                                        return True
                                else:
                                    self.previous_token()
                                    self.previous_token()
                                    self.previous_token()
                                    self.previous_token()
                                    self.previous_token()
                                    self.previous_token()
                            else:
                                self.previous_token()
                                self.previous_token()
                                self.previous_token()
                                self.previous_token()
                                self.previous_token()
                        else:
                            self.previous_token()
                            self.previous_token()
                            self.previous_token()
                            self.previous_token()
                    else:
                        self.previous_token()
                        self.previous_token()
                        self.previous_token()
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
        
        return False
    
    def all(self, exp):
        first = True
        while (self.expecting > exp):
            if first: 
                first = False
            else:
                self.next_token()

            if self.if_statement():
                print(f"Success: if.")
                # TODO: buildar ast
            elif self.attr_expression():
                print(f"Success: attr_expression.")
                # TODO: buildar ast
            elif self.init_expression():
                print(f"Success: init_expression.")
                # TODO: buildar ast
            # TODO: adicionar while, for, else, else if, output(), input()
            else:
                print(f"ERROR: No matching rule for {self.token.to_string()}")
                sys.exit()

        return True

    def type_(self):
        if self.token.get_type() in ['number_reserved', 'bool_reserved', 'string_reserved']:
            return True

        return False

    def attr_expression(self):
        if self.type_():
            self.next_token()
            if self.token.get_type() == 'id':
                self.next_token()
                if self.token.get_type() == 'attr':
                    self.next_token()
                    if self.value():
                        return True
                    else:
                        self.previous_token()
                        self.previous_token()
                        self.previous_token()
                else:
                    self.previous_token()
                    self.previous_token()
        
            else:
                self.previous_token()
        elif self.token.get_type() == 'id':
            self.next_token()
            if self.token.get_type() == 'attr':
                self.next_token()
                if self.value():
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
    
        return False
        
    def init_expression(self):
        print(self.token.to_string())
        if self.type_():
            self.next_token()
            if self.token.get_type() == 'id':
                return True
            else:
                self.previous_token()
        
        return False