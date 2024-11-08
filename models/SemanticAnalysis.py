from models import SymbolTable

class SemanticAnalysis:
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def analyze(self, node):
        # Inicio da análise no nó raiz
        self._analyze_node(node)
    
    def _analyze_node(self, node):
        # Lógica para diferentes tipos de nós da AST
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
        else:
            # Percorre os nós filhos recursivamente
            for child in node.nodes:
                self._analyze_node(child)
    
    def _analyze_attr_expression(self, node):
        # Verifica declaração e tipo de uma expressão de atribuição
        var_type = None
        var_name = None
        for child in node.nodes:
            if child.name == "type":
                var_type = child.nodes[0].name
            elif child.name == "id":
                var_name = child.nodes[0].name
            elif child.name == "value":
                self._analyze_expression(child)
        
        if var_name and var_type:
            self.symbol_table.declare_variable(var_name, var_type)
        else:
            raise Exception("Semantic Error: Invalid attr_expression structure.")

    def _analyze_init_expression(self, node):
        # Análise de declaração de variável
        var_type = None
        var_name = None
        for child in node.nodes:
            if child.name == "type":
                var_type = child.nodes[0].name
            elif child.name == "id":
                var_name = child.nodes[0].name
        
        if var_name and var_type:
            self.symbol_table.declare_variable(var_name, var_type)
        else:
            raise Exception("Semantic Error: Invalid init_expression structure.")

    def _analyze_if_statement(self, node):
        # Análise da condição do 'if'
        for child in node.nodes:
            if child.name == "condition":
                self._analyze_expression(child)
            elif child.name == "all":
                self._analyze_node(child)

    def _analyze_for_statement(self, node):
        # Análise de uma estrutura 'for'
        for child in node.nodes:
            if child.name == "id":
                self.symbol_table.get_variable_type(child.nodes[0].name)  # Valida se a variável está declarada
            elif child.name == "all":
                self._analyze_node(child)

    def _analyze_while_statement(self, node):
        # Análise da condição do 'while'
        for child in node.nodes:
            if child.name == "condition":
                self._analyze_expression(child)
            elif child.name == "all":
                self._analyze_node(child)

    def _analyze_expression(self, node):
        # Verifica o tipo e estrutura das expressões (simplificado)
        for child in node.nodes:
            if child.name == "id":
                self.symbol_table.get_variable_type(child.nodes[0].name)  # Verifica se a variável existe
            elif child.name in ["add", "sub", "mul", "div"]:
                # Pode expandir com verificações de tipos compatíveis
                pass
            else:
                self._analyze_expression(child)