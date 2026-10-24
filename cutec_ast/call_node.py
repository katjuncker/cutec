from cutec_ast.node import Node

class CallNode(Node):
    action: Node
    arguments: list[Node]

    def __init__(self, action: Node, arguments: list[Node]|None = None):
        self.action = action
        if arguments is None:
            arguments = []
        self.arguments = arguments
        super().__init__()

    def __str__(self) -> str:
        arg_str = ', '.join([str(arg) for arg in self.arguments])
        return '( ' + str(self.action) + '(' + arg_str + ')' + ' )'
