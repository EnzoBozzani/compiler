from models import Tree, Symbol, Token

class SemanticAnalysis():
    def __init__(self, trees: list[Tree]):
        self.symbols: list[Symbol] = []
        for tree in trees:
            if tree.type == 'attr_expression':
                self.symbols.append(Symbol(type=tree.nodes[0].get_lexem(), name=tree.nodes[1].get_lexem(), scope=''))
                
            
    
    def symbol_exists(self, tree: Tree):
        exists = False
        for s in self.symbols:
            for token in tree.nodes:
                if token.get_lexem() == s.name:
                    print('Exists')

        

