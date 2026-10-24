from cutec_ast.node import Node

class ChaseNode(Node):
    catches: list[Node]
    escape: Node|None

    def __init__(self, catches: list[Node], escape: Node|None = None):
        self.catches = catches
        self.escape = escape
        super().__init__()

    def __str__(self) -> str:
        catches_str = ''.join(['\t' + str(c) + '\n' for c in self.catches])
        if self.escape:
            return 'chase\n' + catches_str + str(self.escape)
        else:
            return 'chase\n' + catches_str