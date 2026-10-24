from cutec_ast.node import Node

class ChaseNode(Node):
    catches: list[Node]
    escape: Node|None

    def __init__(self, catches: list[Node], escape: Node|None = None):
        self.catches = catches
        self.escape = escape
        super().__init__()
