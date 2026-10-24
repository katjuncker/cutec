from cutec_ast.node import Node

class UnaryOp(Node):
    right: Node
    op: str

    def __init__(self, op: str, right: Node):
        self.op = op
        self.right = right
        super().__init__()
