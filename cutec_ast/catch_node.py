from cutec_ast.node import Node

class CatchNode(Node):
    condition: Node
    action: Node

    def __init__(self, condition: Node, action: Node):
        self.condition = condition
        self.action = action
        super().__init__()

    def __str__(self) -> str:
        return '(' + str(self.condition) + ') ' + str(self.action)
