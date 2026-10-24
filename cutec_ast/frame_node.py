from cutec_ast.node import Node

class FrameNode(Node):
    nodes: list[Node]

    def __init__(self, nodes=None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        super().__init__()

    def __str__(self) -> str:
        return '{\n' + ''.join(['\t' + str(n) + '\n' for n in self.nodes]) + '}'
