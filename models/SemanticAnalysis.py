import sys

from models import SymbolTable, Node

class SemanticAnalysis:
    def __init__(self, root: Node):
        self.symbol_table = SymbolTable()
        self.translation = ""

        self._analyze_node(root)

        print(self.translation)
    
    def _analyze_node(self, node):
        if node.name == "attr_expression":
            self._analyze_attr_expression(node)
        elif node.name == "init_expression":
            self._analyze_init_expression(node)
        elif node.name == "if":
            self._analyze_if_statement(node)
        elif node.name == "for":
            self._analyze_for_statement(node)
        elif node.name == "while":
            self._analyze_while_statement(node)
        elif node.name == 'output':
            self._analyze_output(node)
        else:
            for child in node.nodes:
                self._analyze_node(child)

    def _analyze_attr_expression(self, node):
        var_type = None
        var_name = None
        for child in node.nodes:
            if child.name == "type":
                var_type = child.nodes[0].name
            elif child.name == "id":
                var_name = child.nodes[0].name
                self.translate(child)
            elif child.name == 'attr':
                self.translate(child)
            elif child.name == "value":
                self._analyze_expression(child, end="\n")
        
        if var_name and var_type:
            self.symbol_table.declare_variable(var_name, var_type)
        elif var_name and not var_type:
            self.symbol_table.get_variable_type(var_name)
        else:
            print(f"ERRO SEMÂNTICO: Atribuição inválida ({[n.name for n in child.nodes ]})")
            sys.exit()

    def _analyze_init_expression(self, node):
        var_type = None
        var_name = None
        for child in node.nodes:
            if child.name == "type":
                var_type = child.nodes[0].name
            elif child.name == "id":
                var_name = child.nodes[0].name
        
        if var_name and var_type:
            self.symbol_table.declare_variable(var_name, var_type)
            self.translate(node)
        else:
            print(f"ERRO SEMÂNTICO: Inicialização inválida ({child.name})")
            sys.exit()

    def _analyze_if_statement(self, node):
        for child in node.nodes:
            if child.name in ['if_reserved', "op", 'cp', 'open_curly_braces', 'close_curly_braces']:
                self.translate(child)
            elif child.name == "condition":
                self._analyze_expression(child)
            elif child.name == "all":
                self._analyze_node(child)
    
    def _analyze_output(self, node):
        for child in node.nodes:
            if child.name in ['output_reserved']:
                self.translate(child)
            else:
                self._analyze_expression(child, end=")\n")


    def _analyze_for_statement(self, node):
        for child in node.nodes:
            if child.name in ['for_reserved', "op", 'cp', 'open_curly_braces', 'close_curly_braces', 'in_reserved']:
                self.translate(child)
            elif child.name == "id":
                self.symbol_table.get_variable_type(child.nodes[0].name) 
                self.translate(child)
            elif child.name == "all":
                self._analyze_node(child)

    def _analyze_while_statement(self, node):
        for child in node.nodes:
            if child.name in ['while_reserved', "op", 'cp', 'open_curly_braces', 'close_curly_braces']:
                self.translate(child)
            elif child.name == "condition":
                self._analyze_expression(child)
            elif child.name == "all":
                self._analyze_node(child)

    def _analyze_expression(self, node, end = ""):        
        for child in node.nodes:
            if child.name == "id":
                var_name = child.nodes[0].name
                self.symbol_table.get_variable_type(var_name)
                self.translate(child, end=end)
            elif child.name in ["number", "string", "add", "sub", "mult", "div", "op", "cp", "true", "false", "gt", "equal", "gte", "lte", "lt"]:
                self.translate(child, end=end if len(node.nodes) == 1 else " ")   
            else:
                self._analyze_expression(child, end=end)
    
    def translate(self, node: Node, end = ""):
        map = {
            'if_reserved': 'if ',
            'else_reserved': 'else',
            'number_reserved': '',
            'string_reserved': '',
            'while_reserved': 'while',
            'for_reserved': 'for',
            'output_reserved': 'print(',
            'input_reserved': 'input()',
            'in_reserved': 'in',
            'bool_reserved': 'bool',
            'true': 'True',
            'false': 'False',
            'op': '(',
            'cp': ')',
            'gt': '>',
            'attr': '= ',
            'equal': '==',
            'gte': '>=',
            'lte': '<=',
            'lt': '<',
            'open_curly_braces': ':\n  ',
            'close_curly_braces': '\n\r',
            'string': node.nodes[0].name,
            'add': '+',
            'sub': '-',
            'mult': '*',
            'div': '/',
            'number': node.nodes[0].name,
            'id': f"{node.nodes[0].name} ",
            'init_expression': f"{node.nodes[1].nodes[0].name} = None\n" if node.name == 'init_expression' else ""
        }

        self.translation += f"{map[node.name]}{end}" or ""


