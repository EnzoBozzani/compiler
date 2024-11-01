class SyntaticAnalysis():
    def __init__(self, tokens: list[str]):
        self.tokens = tokens

        self.token = self.next_token()

        while len(self.tokens) > 0:
            if self.math_e():
                print('Success')
            elif self.math_e_():
                print('Success')
            elif self.math_t():
                print('Success')                      

    def next_token(self):
        return self.tokens.pop(0)
    
    def math_e(self):
        if self.math_t():
            self.token = self.next_token()
            if self.math_e_():
                return True
        
        return False

    def math_e_(self):
        if self.token in ['add', 'sub']:
            self.token = self.next_token()
            if self.math_t():
                self.token = self.next_token()
                if self.math_e_():
                    return True
        
        return True

    def math_t(self):
        if self.math_f():
            self.token = self.next_token()
            if self.math_t_():
                return True
        
        return False

    def math_t_(self):
        if self.token in ['mult', 'div']:
            self.token = self.next_token()
            if self.math_f():
                self.token = self.next_token()
                if self.math_t_():
                    return True
        
        return True
    
    def math_f(self):
        raise NotImplementedError()
    
    def math_n(self):
        raise NotImplementedError()
    
    def math_n_(self):
        raise NotImplementedError()
    
    def math_d(self):
        raise NotImplementedError()
    
    def value(self):
        raise NotImplementedError()

    def condition(self):
        raise NotImplementedError()
    
    def if_statement(self):
        raise NotImplementedError()
    
    def all(self):
        raise NotImplementedError()
    
    def type_(self):
        raise NotImplementedError()

    def attr_expression(self):
        raise NotImplementedError()
    
    def init_expression(self):
        raise NotImplementedError()