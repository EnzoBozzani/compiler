from models import Token

class Tree():
    def __init__(self, rule: str, tokens: list[Token]):
        self.type = rule
        self.tokens = [t for t in tokens]

    def to_string(self):
        print(self.type)
        for t in self.tokens:
            print(t.get_lexem(), end=' ')
        print()
        for t in self.tokens:
            print(t.get_type(), end=' ')
        print()
        print()