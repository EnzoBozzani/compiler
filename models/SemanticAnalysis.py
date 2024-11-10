import sys

from models import SymbolTable, Node

class SemanticAnalysis:
    def __init__(self, root: Node):
        self.symbol_table = SymbolTable()
        self.translation = ""

        self._analyze_node(root)

        print(self.translation)

    def error(self, message: str):
        print(f"ERRO SEMÂNTICO: {message}")
        sys.exit()
    
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
            var_type = self.symbol_table.get_variable_type(var_name)
            current = node.nodes[2]
            previous = node
            while len(current.nodes) > 0:
                previous = current
                current = current.nodes[0]
            
            if var_type == 'number_reserved':
                if previous.name != 'number' and previous.name != 'id':
                    self.error(f'Não é possível atribuir {previous.name} ({current.name}) para variável de tipo number ({var_name})')
            elif var_type == 'string_reserved' and previous.name != 'id':
                if previous.name != 'string' and previous.name != 'id':
                    self.error(f'Não é possível atribuir {previous.name} ({current.name}) para variável de tipo string ({var_name})')
            elif var_type == 'bool_reserved':
                if previous.name != 'true' and previous.name != 'false':
                    self.error(f'Não é possível atribuir {previous.name} ({current.name}) para variável de tipo bool ({var_name})')
        else:
            self.error(f"Atribuição inválida")

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
            self.error(f"Inicialização")

    def _analyze_if_statement(self, node):
        for child in node.nodes:
            if child.name in ['if_reserved', "op", 'cp', 'open_curly_braces', 'close_curly_braces', 'else_reserved']:
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


    def _analyze_for_statement(self, node: Node):
        for i, child in enumerate(node.nodes):
            if child.name in ['for_reserved', 'open_curly_braces', 'close_curly_braces', 'in_reserved']:
                self.translate(child)
            elif i == 2:
                self.symbol_table.declare_variable(child.nodes[0].name, var_type='number') 
                self.translate(child)
            elif i == 4:
                self.translate(node.nodes[4], special="id_or_number")
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
            elif child.name in ["number", "string", "add", "sub", "mult", "div", "op", "cp", "true", "false", "gt", "equal", "gte", "lte", "lt", "input_reserved"]:
                self.translate(child, end=end if len(node.nodes) == 1 else " ")   
            else:
                self._analyze_expression(child, end=end)
    
    def translate(self, node: Node, end = "", special = None):
        if special is not None and special == 'id_or_number':
            if node.name == 'id':
                var_type = self.symbol_table.get_variable_type(node.nodes[0].name)
                
                if var_type != 'number_reserved':
                    self.error(f'Variável no loop for deve ser do tipo number')

        map = {
            'if_reserved': 'if ',
            'else_reserved': 'else',
            'number_reserved': '',
            'string_reserved': '',
            'while_reserved': 'while',
            'for_reserved': 'for ',
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
            'id_or_number': f' range({node.nodes[0].name})',
            'for_p': '',
            'number': node.nodes[0].name,
            'id': f"{node.nodes[0].name} ",
            'init_expression': f"{node.nodes[1].nodes[0].name} = None\n" if node.name == 'init_expression' else ""
        }

        self.translation += f"{map[node.name if special is None else special]}{end}" or ""


