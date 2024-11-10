import sys

from models import Token, Tree, Node

class SyntaticAnalysis():
    def __init__(self, tokens: list[Token]):
        if len(tokens) == 0:
            print("ERRO: Arquivo vazio")
            sys.exit()

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
            if self.statement(self.root):
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
        print(f"ERRO SINTÁTICO: Nenhuma regra encontrada para {self.token.to_string()}")
        sys.exit()


    def token_in(self, args: list[str], node: Node | None):
        if self.token is None: return

        if node is None:
            return self.token.get_type() in args

        if self.token.get_type() in args:
            new = Node(name=self.token.get_type())
            new.add_node(Node(name=self.token.get_lexem()))
            node.add_node(new)
            return True

        return False
    
    def statement(self, root: Node):
        if self.if_statement(root):
            return True
        elif self.attr_expression(root):
            return True
        elif self.init_expression(root):
            return True
        elif self.for_statement(root):
            return True
        elif self.while_statement(root):
            return True
        elif self.output(root):
            return True
        else:
            return False
        
    def expr(self, root: Node):
        node = Node("expr")
        if self.factor(node):
            self.next_token()
            if self.expr_(node):
                root.add_node(node)
                return True
            else:
                self.previous_token()

        return False
    
    def expr_(self, root: Node):
        node = Node("expr'")
        if self.token_in(['add', 'sub', 'mult', 'div'], node):
            self.next_token()
            if self.factor(node):
                self.next_token()
                if self.expr_(node):
                    root.add_node(node)
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
        
        root.add_node(node)
        self.previous_token()
        return True

    def factor(self, root: Node):
        node = Node("factor")
        if self.token_in(['number', 'id'], node):
            root.add_node(node)
            return True
        elif self.token_in(['op'], node):
            self.next_token()
            if self.expr(node):
                self.next_token()
                if self.token_in(['cp'], node):
                    root.add_node(node)
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()

        return False    


    def value(self, root: Node):
        node = Node("value")
        if self.expr(node):
            root.add_node(node)
            return True
        elif self.token_in(['id', 'true', 'false', 'string'], node):
            root.add_node(node)
            return True
        elif self.input(node):
            root.add_node(node)
            return True
        
        return False


    def condition(self, root: Node):
        node = Node("condition")
        if self.value(node):
            self.next_token()
            if self.condition_(node):
                root.add_node(node)
                return True
            else:
                self.previous_token()
        
        return False
    

    def condition_(self, root: Node):
        node = Node("condition'")
        if self.comparison_operator(node):
            self.next_token()
            if self.value(node):
                root.add_node(node)
                return True
            else:
                self.previous_token()

        self.previous_token()
        root.add_node(node)
        return True
    

    def comparison_operator(self, root: Node):
        node = Node("comparison_operator")
        if self.token_in(['gt', 'equal', 'gte', 'lte', 'lt'], node):
            root.add_node(node)
            return True
        
        return False
    

    def if_statement(self, root: Node):
        node = Node("if")
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
                                                    root.add_node(node)
                                                    return True
                                    else:
                                        if len(self.tokens) > 0: self.previous_token()
                                        root.add_node(node)
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
        first = True
        while (self.expecting > exp):
            if first: 
                first = False
            else:
                self.next_token()

            if self.statement(node):
                continue
            else:
                self.error()

        root.add_node(node)
        return True


    def type_(self, root: Node):
        node = Node("type")
        if self.token_in(['number_reserved', 'bool_reserved', 'string_reserved'], node):
            root.add_node(node)
            return True

        return False


    def attr_expression(self, root: Node):
        node = Node("attr_expression")
        if self.type_(node):
            self.next_token()
            if self.token_in(['id'], node):
                self.next_token()
                if self.token_in(['attr'], node):
                    self.next_token()
                    if self.value(node):
                        root.add_node(node)
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
                    root.add_node(node)
                    return True
                else:
                    self.previous_token()
                    self.previous_token()
            else:
                self.previous_token()
    
        return False
        

    def init_expression(self, root: Node):
        node = Node("init_expression")
        if self.type_(node):
            self.next_token()
            if self.token_in(['id'], node):
                root.add_node(node)
                return True
            else:
                self.previous_token()
        
        return False
    

    def for_statement(self, root: Node):
        node = Node("for")
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
                                            root.add_node(node)
                                            return True
                                        
        return False
    
    def while_statement(self, root: Node):
        node = Node("while")
        if self.token_in(['while_reserved'], node):
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
                                    root.add_node(node)
                                    return True
                                        
        return False
    
    def output(self, root: Node):
        node = Node("output")
        if self.token_in(['output_reserved'], node):
            self.next_token()
            if self.value(node):
                root.add_node(node)
                return True
        
        return False

    def input(self, root: Node):
        node = Node("input")
        if self.token_in(['input_reserved'], node):
            root.add_node(node)
            return True
        
        return False