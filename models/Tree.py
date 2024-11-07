from models import Token

class Tree():
    def __init__(self, rule: str, nodes: list[Token]):
        self.type = rule
        self.nodes = [t for t in nodes]

    def to_string(self):
        print(self.type)
        for t in self.nodes:
            print(t.to_string(), end=' ')
        print()
        print()