from models import Token, Symbol

class SemanticAnalysis():
    def __init__(self, trees: list[list[Token]]):
        self.symbols: list[Symbol] = []
        for tree in trees:
            for token in tree:
                raise NotImplementedError()
