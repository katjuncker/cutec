from cutec_ast.node import Node

class EscapeNode(Node):
    timeout: Node
    action: Node

    def __init__(self, timeout: Node, action: Node):
        self.timeout = timeout
        self.action = action
        super().__init__()
