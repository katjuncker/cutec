from cutec_ast.node import Node

class ActionNode(Node):
    frame: Node

    def __init__(self, frame: Node):
        self.frame = frame
        super().__init__()
