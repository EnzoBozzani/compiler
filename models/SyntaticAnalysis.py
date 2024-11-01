from models import Token

class SyntaticAnalysis():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.previous = []
        print([t.to_string() for t in tokens])

        self.run()

    def run(self):
        while len(self.tokens) > 0:
            self.token = self.next_token()
            if self.if_statement():
                print(f"Success: if.")
            elif self.attr_expression():
                print(f"Success: attr_expression.")
            elif self.init_expression():
                print(f"Success: init_expression.")
            # adicionar aqui outras expressões como for, while
            else:
                print(f"Error: No matching rule for {self.token.to_string()}")
                break 

               

    def next_token(self):
        t = self.tokens.pop(0)
        self.previous.append(t)
        return t
    
    def previous_token(self):
        self.tokens.insert(0, self.previous.pop(0)) 
    
    def error(self, rule: str):
        self.errors.append(f"Not expected: {self.token}. Rule: {rule}")
    
    def math_e(self):
        if self.math_t():
            self.token = self.next_token()
            if self.math_e_():
                return True
            else:
                self.previous_token()
    
        return False

    def math_e_(self):
        if self.token.get_type() in ['add', 'sub']:
            self.token = self.next_token()
            if self.math_t():
                self.token = self.next_token()
                if self.math_e_():
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
        
        return True

    def math_t(self):
        if self.math_f():
            self.token = self.next_token()
            if self.math_t_():
                return True
            else:
                self.previous_token()
        
        return False

    def math_t_(self):
        if self.token.get_type() in ['mult', 'div']:
            self.token = self.next_token()
            if self.math_f():
                self.token = self.next_token()
                if self.math_t_():
                    return True
                else: 
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
        
        return True
    
    def math_f(self):
        if self.token.get_type() == 'op':
            self.token = self.next_token()
            if self.math_e():
                self.token = self.next_token()
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
            self.token = self.next_token()
            if self.math_n_():
                return True
            else:
                self.previous_token()
        
        return False
    
    def math_n_(self):
        if self.math_d():
            self.token = self.next_token()
            if self.math_n_():
                return True
            else: 
                self.previous_token()
        
        return True
    
    def math_d(self):
        if self.token.get_type() in ['id', 'number']:
            return True
        
        return False
    
    def value(self):
        if self.token.get_type() in ['number', 'id', 'true', 'false', 'string']:
            return True
        elif self.math_e():
            return True
        
        return False

    def condition(self):
        if self.value():
            self.token = self.next_token()
            if self.condition_():
                return True
            else:
                self.previous_token()
        
        return False
    
    def condition_(self):
        if self.comparison_operator():
            self.token = self.next_token()
            if self.value():
                return True
            else:
                self.previous_token()
        
        return True
    
    def comparison_operator(self):
        if self.token.get_type() in ['gt', 'equal', 'gte', 'lte', 'lt']:
            return True
        
        return False
    
    def if_statement(self):
        if self.token.get_type() == 'if_reserved':
            self.token = self.next_token()
            if self.token.get_type() == 'op':
                self.token = self.next_token()
                if self.condition():
                    self.token = self.next_token()
                    if self.token.get_type() == 'cp':
                        self.token = self.next_token()
                        if self.token.get_type() == 'open_curly_braces':
                            self.token = self.next_token()
                            if self.all():
                                self.token = self.next_token()
                                if self.token.get_type() == 'close_curly_braces':
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
    
    def all(self):
        expecting = 1

    def type_(self):
        if self.token.get_type() in ['number_reserved', 'bool_reserved', 'string_reserved']:
            return True

        return False

    def attr_expression(self):
        if self.type_():
            self.token = self.next_token()
            if self.token.get_type() == 'id':
                self.token = self.next_token()
                if self.token.get_type() == 'attr':
                    self.token = self.next_token()
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
            self.token = self.next_token()
            if self.token.get_type() == 'attr':
                self.token = self.next_token()
                if self.value():
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
        
        return False
        
    def init_expression(self):
        if self.type_():
            self.token = self.next_token()
            if self.token.get_type() == 'id':
                return True
            else:
                self.previous_token()
        
        return False