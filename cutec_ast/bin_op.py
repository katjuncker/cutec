from cutec_ast.node import Node

class BinOp(Node):
    left: Node
    right: Node
    op: str

    def __init__(self, op: str, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right
        super().__init__()

    def __str__(self) -> str:
        return '(' + str(self.left) + ' ' + self.op + ' ' + str(self.right) + ')'