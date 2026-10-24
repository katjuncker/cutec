from cutec_ast.node import Node

class UnaryOp(Node):
    right: Node
    op: str

    def __init__(self, op: str, right: Node):
        self.op = op
        self.right = right
        super().__init__()

    def __str__(self) -> str:
        return '(' + self.op + ' ' + str(self.right) + ')'