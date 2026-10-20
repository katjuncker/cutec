from cutec_ast.node import Node

class FrameNode(Node):
    nodes: list[Node]

    def __init__(self, nodes=None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        super().__init__()
