from cutec_ast.node import Node

class ActionNode(Node):
    frame: Node
    params: list[Node]

    def __init__(self, frame: Node, params: list[Node]|None = None):
        if params is None:
            params = []
        self.params = params
        self.frame = frame
        super().__init__()
