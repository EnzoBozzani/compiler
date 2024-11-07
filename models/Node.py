class Node:
    def __init__(self, name, enter="", exit=""):
        self.name = name
        self.nodes = []
        self.enter = enter
        self.exit = exit

    def add_node(self, new_node):
        self.nodes.append(new_node)

    def add_node_by_name(self, node_name):
        new_node = Node(node_name)
        self.nodes.append(new_node)
        return new_node

    def add_node_with_text(self, enter, node_name, exit):
        new_node = Node(node_name, enter, exit)
        self.nodes.append(new_node)
        return new_node

    def __str__(self):
        return f"{self.enter} {self.name} {self.exit}"

    def get_tree(self):
        print("AST")
        buffer = []
        self._print(buffer, "", "")
        return ''.join(buffer)

    def _print(self, buffer, prefix, children_prefix):
        buffer.append(f"{prefix}{self.name}\n")
        for i, node in enumerate(self.nodes):
            if i < len(self.nodes) - 1:
                node._print(buffer, children_prefix + "+-- ", children_prefix + "|   ")
            else:
                node._print(buffer, children_prefix + "+-- ", children_prefix + "    ")
