from cutec_ast.node import Node

class AssignNode(Node):
    obj: Node|None
    name: str
    value: Node

    def __init__(self, name: str, value: Node, obj: Node|None = None):
        self.name = name
        self.value = value
        self.obj = obj
        super().__init__()

    def __str__(self) -> str:
        if self.obj:
            return str(self.obj) + '.' + self.name + ' = ' + str(self.value)
        else:
            return self.name + ' = ' + str(self.value)
