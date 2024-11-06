import sys

from models import Token, Tree

class SyntaticAnalysis():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.previous_tokens = []
        self.expecting = 0
        self.previous = None
        self.trees: list[Tree] = []
        self.token = self.tokens.pop(0)
        self.first_exec = True

        self.run()


    def run(self):
        first = True
        while len(self.tokens) > 0:
            if first: 
                first = False
            else:
                self.next_token()
            if self.if_statement():
                self.success('if')
            elif self.attr_expression():
                self.success('attr_expression')
            elif self.init_expression():
                self.success('init_expression')
            elif self.for_statement():
                self.success('for')
            elif self.while_statement():
                self.success('while')
            elif self.output():
                self.success('output')
            else:
                self.error()


    def next_token(self):
        if len(self.tokens) <= 0:
            if self.previous is not None: self.previous_tokens.insert(0, self.previous)
            self.previous = self.token
            self.token = None
            return
        if self.previous is not None: self.previous_tokens.insert(0, self.previous)
        self.previous = self.token
        self.token = self.tokens.pop(0)
        if self.token_in(['open_curly_braces']): self.expecting += 1
        if self.token_in(['close_curly_braces']): self.expecting -= 1
        # print(f"TOKEN: {self.token.to_string()}")
    

    def previous_token(self):
        if self.token is not None: self.tokens.insert(0, self.token)
        self.token = self.previous
        self.previous = self.previous_tokens.pop(0) if len(self.previous_tokens) > 0 else None
        if self.token_in(['open_curly_braces']): self.expecting -= 1
        if self.token_in(['close_curly_braces']): self.expecting += 1
    

    def error(self):
        print(f"ERROR: Nenhuma regra encontrada para {self.token.to_string()}")
        sys.exit()

    
    def success(self, rule: str):
        self.build_tree(rule)

    
    def build_tree(self, rule):
        tokens = []
        if self.first_exec:
            for i in range(len(self.previous_tokens) - 1, -1, -1):
                tokens.append(self.previous_tokens[i])
            tokens.append(self.previous)
            tokens.append(self.token)
            self.first_exec = False
        else:
            for i in range(len(self.previous_tokens) - 3, -1, -1):
                tokens.append(self.previous_tokens[i])
            tokens.append(self.previous)
            tokens.append(self.token)

        self.trees.append(Tree(rule=rule, tokens=tokens))
        self.previous_tokens = []


    def token_in(self, args: list[str]):
        if self.token is None: return

        return self.token.get_type() in args
    

    def math_e(self):
        if self.math_t():
            self.next_token()
            if self.math_e_():
                return True
            else:
                self.previous_token()
        
        return False


    def math_e_(self):
        if self.token_in(['add', 'sub']):
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
        if self.token_in(['mult', 'div']):
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
        if self.token_in(['op']):
            self.next_token()
            if self.math_e():
                self.next_token()
                if self.token_in(['cp']):
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
        if self.token_in(['id', 'number']):
            return True
        
        return False
    

    def value(self):
        if self.token_in(['id', 'number']):
            self.next_token()
            if self.token_in(['add', 'sub', 'div', 'mult']):
                self.next_token()
                if self.math_e():
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()

        if self.token_in(['number', 'id', 'string', 'true', 'false', 'input_reserved']):
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
        if self.token_in(['gt', 'equal', 'gte', 'lte', 'lt']):
            return True
        
        return False
    

    def if_statement(self):
        if self.token_in(['if_reserved']):
            self.next_token()
            if self.token_in(['op']):
                self.next_token()
                if self.condition():
                    self.next_token()
                    if self.token_in(['cp']):
                        self.next_token()
                        if self.token_in(['open_curly_braces']):
                            self.next_token()
                            if self.all(self.expecting - 1):
                                self.next_token()
                                if self.token_in(['close_curly_braces']):
                                    self.next_token()
                                    if self.token_in(['else_reserved']):
                                        self.next_token()
                                        if self.token_in(['open_curly_braces']):
                                            self.next_token()
                                            if self.all(self.expecting - 1):
                                                self.next_token()
                                                if self.token_in(['close_curly_braces']):
                                                    return True
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
                self.success('if')
            elif self.attr_expression():
                self.success('attr_expression')
            elif self.init_expression():
                self.success('init_expression')
            elif self.for_statement():
                self.success('for')
            elif self.while_statement():
                self.success('while')
            elif self.output():
                self.success('output')
            else:
                self.error()

        return True


    def type_(self):
        if self.token_in(['number_reserved', 'bool_reserved', 'string_reserved']):
            return True

        return False


    def attr_expression(self):
        if self.type_():
            self.next_token()
            if self.token_in(['id']):
                self.next_token()
                if self.token_in(['attr']):
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
        elif self.token_in(['id']):
            self.next_token()
            if self.token_in(['attr']):
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
        if self.type_():
            self.next_token()
            if self.token_in(['id']):
                return True
            else:
                self.previous_token()
        
        return False
    

    def for_statement(self):
        if self.token_in(['for_reserved']):
            self.next_token()
            if self.token_in(['op']):
                self.next_token()
                if self.token_in(['id']):
                    self.next_token()
                    if self.token_in(['in_reserved']):
                        self.next_token()
                        if self.token_in(['id', 'number']):
                            self.next_token()
                            if self.token_in(['cp']):
                                self.next_token()
                                if self.token_in(['open_curly_braces']):
                                    self.next_token()
                                    if self.all(self.expecting - 1):
                                        self.next_token()
                                        if self.token_in(['close_curly_braces']):
                                            return True
                                        
        return False
    
    def while_statement(self):
        if self.token_in(['while_reserved']):
            self.next_token()
            if self.token_in(['op']):
                self.next_token()
                if self.condition():
                    self.next_token()
                    if self.token_in(['cp']):
                        self.next_token()
                        if self.token_in(['open_curly_braces']):
                            self.next_token()
                            if self.all(self.expecting - 1):
                                self.next_token()
                                if self.token_in(['close_curly_braces']):
                                    return True
                                        
        return False
    
    def output(self):
        if self.token_in(['output_reserved']):
            self.next_token()
            if self.value():
                return True
        
        return False