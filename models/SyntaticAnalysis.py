import sys

from models import Token, Tree, Node

class SyntaticAnalysis():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.previous_tokens = []
        self.expecting = 0
        self.previous = None
        self.internal_blocks = []
        self.token = self.tokens.pop(0)
        self.first_exec = True

        self.root = Node("program")
        self.tree = Tree(self.root)

        self.run()


    def run(self):
        first = True
        while len(self.tokens) > 0:
            if first: 
                first = False
            else:
                self.next_token()
            if self.if_statement(self.root):
                # self.build_tree('if')
                continue
            elif self.attr_expression(self.root):
                # self.build_tree('attr_expression')
                continue
            elif self.init_expression(self.root):
                # self.build_tree('init_expression')
                continue
            elif self.for_statement(self.root):
                # self.build_tree('for')
                continue
            elif self.while_statement(self.root):
                # self.build_tree('while')
                continue
            elif self.output(self.root):
                # self.build_tree('output')
                continue
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
        if self.token_in(['open_curly_braces'], None): self.expecting += 1
        if self.token_in(['close_curly_braces'], None): self.expecting -= 1
    

    def previous_token(self):
        if self.token is not None: self.tokens.insert(0, self.token)
        self.token = self.previous
        self.previous = self.previous_tokens.pop(0) if len(self.previous_tokens) > 0 else None
        if self.token_in(['open_curly_braces'], None): self.expecting -= 1
        if self.token_in(['close_curly_braces'], None): self.expecting += 1
    

    def error(self):
        print(f"ERROR: Nenhuma regra encontrada para {self.token.to_string()}")
        sys.exit()
    
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

        self.trees.append(Tree(rule=rule, nodes=tokens))
        self.previous_tokens = []


    def token_in(self, args: list[str], node: Node | None):
        if self.token is None: return

        if node is None:
            return self.token.get_type() in args

        if self.token.get_type() in args:
            node.add_node(Node(name=self.token.get_type()))
            return True

        return False
    

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
    

    def value(self, root: Node):
        node = Node("value")
        root.add_node(node)
        if self.token_in(['id', 'number'], node):
            self.next_token()
            if self.token_in(['add', 'sub', 'div', 'mult'], node):
                self.next_token()
                if self.math_e(node):
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
                return True

        if self.token_in(['string', 'true', 'false', 'input_reserved'], node):
            return True
        elif self.math_e():
            return True
        
        return False


    def condition(self, root: Node):
        node = Node("condition")
        root.add_node(node)
        if self.value(node):
            self.next_token()
            if self.condition_(node):
                return True
            else:
                self.previous_token()
        
        return False
    

    def condition_(self, root: Node):
        node = Node("condition'")
        root.add_node(node)
        if self.comparison_operator(node):
            self.next_token()
            if self.value(node):
                return True
            else:
                self.previous_token()

        self.previous_token()
        return True
    

    def comparison_operator(self, root: Node):
        node = Node("comparison_operator")
        root.add_node(node)
        if self.token_in(['gt', 'equal', 'gte', 'lte', 'lt'], node):
            return True
        
        return False
    

    def if_statement(self, root: Node):
        node = Node("if")
        root.add_node(node)
        if self.token_in(['if_reserved'], node):
            self.next_token()
            if self.token_in(['op'], node):
                self.next_token()
                if self.condition(node):
                    self.next_token()
                    if self.token_in(['cp'], node):
                        self.next_token()
                        if self.token_in(['open_curly_braces'], node):
                            self.next_token()
                            if self.all(self.expecting - 1, node):
                                self.next_token()
                                if self.token_in(['close_curly_braces'], node):
                                    self.next_token()
                                    if self.token_in(['else_reserved'], node):
                                        self.next_token()
                                        if self.token_in(['open_curly_braces'], node):
                                            self.next_token()
                                            if self.all(self.expecting - 1, node):
                                                self.next_token()
                                                if self.token_in(['close_curly_braces'], node):
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
    

    def all(self, exp, root: Node):
        node = Node("all")
        root.add_node(node)
        first = True
        while (self.expecting > exp):
            if first: 
                first = False
            else:
                self.next_token()

            if self.if_statement(node):
                continue
            elif self.attr_expression(node):
                continue
            elif self.init_expression(node):
                continue
            elif self.for_statement(node):
                continue
            elif self.while_statement(node):
                continue
            elif self.output(node):
                continue
            else:
                self.error()

        return True


    def type_(self, root: Node):
        node = Node("type")
        root.add_node(node)
        if self.token_in(['number_reserved', 'bool_reserved', 'string_reserved'], node):
            return True

        return False


    def attr_expression(self, root: Node):
        node = Node("attr_expression")
        root.add_node(node)
        if self.type_(node):
            self.next_token()
            if self.token_in(['id'], node):
                self.next_token()
                if self.token_in(['attr'], node):
                    self.next_token()
                    if self.value(node):
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
        elif self.token_in(['id'], node):
            self.next_token()
            if self.token_in(['attr'], node):
                self.next_token()
                if self.value(node):
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
    
        return False
        

    def init_expression(self, root: Node):
        node = Node("init_expression")
        root.add_node(node)
        if self.type_(node):
            self.next_token()
            if self.token_in(['id'], node):
                return True
            else:
                self.previous_token()
        
        return False
    

    def for_statement(self, root: Node):
        node = Node("for")
        root.add_node(node)
        if self.token_in(['for_reserved'], node):
            self.next_token()
            if self.token_in(['op'], node):
                self.next_token()
                if self.token_in(['id'], node):
                    self.next_token()
                    if self.token_in(['in_reserved'], node):
                        self.next_token()
                        if self.token_in(['id', 'number'], node):
                            self.next_token()
                            if self.token_in(['cp'], node):
                                self.next_token()
                                if self.token_in(['open_curly_braces'], node):
                                    self.next_token()
                                    if self.all(self.expecting - 1, node):
                                        self.next_token()
                                        if self.token_in(['close_curly_braces'], node):
                                            return True
                                        
        return False
    
    def while_statement(self, root: Node):
        node = Node("while")
        root.add_node(node)
        if self.token_in(['while_reserved'], node):
            self.next_token()
            if self.token_in(['op'], node):
                self.next_token()
                if self.condition():
                    self.next_token()
                    if self.token_in(['cp'], node):
                        self.next_token()
                        if self.token_in(['open_curly_braces'], node):
                            self.next_token()
                            if self.all(self.expecting - 1):
                                self.next_token()
                                if self.token_in(['close_curly_braces'], node):
                                    return True
                                        
        return False
    
    def output(self, root: Node):
        node = Node("while")
        root.add_node(node)
        if self.token_in(['output_reserved'], node):
            self.next_token()
            if self.value(node):
                return True
        
        return False