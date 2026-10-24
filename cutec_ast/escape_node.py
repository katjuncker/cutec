from cutec_ast.node import Node

class EscapeNode(Node):
    timeout: Node
    action: Node

    def __init__(self, timeout: Node, action: Node):
        self.timeout = timeout
        self.action = action
        super().__init__()

    def __str__(self) -> str:
        return 'escape (' + str(self.timeout) + ')' + ' {\n'+ str(self.action) + '}'
