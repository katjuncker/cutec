from cutec_ast.node import Node

class AssignNode(Node):
    name: str
    value: Node

    def __init__(self, name: str, value: Node):
        self.name = name
        self.value = value
        super().__init__()
