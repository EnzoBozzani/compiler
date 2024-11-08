from models import Node

class Tree:
    def __init__(self, root=None):
        self.root: Node = root

    def set_root(self, node):
        self.root = node

    def pre_order(self):
        if self.root:
            self._pre_order(self.root)
        print("")

    def print_code(self):
        if self.root:
            self._print_code(self.root)
        print("")

    def _pre_order(self, node):
        print(node, end="")
        for n in node.nodes:
            self._pre_order(n)

    def _print_code(self, node):
        print(node.enter, end="")
        if not node.nodes:
            print(node, end="")
        for n in node.nodes:
            self._print_code(n)
        print(node.exit, end="")

    def print_tree(self):
        if self.root:
            print(self.root.get_tree())
            
