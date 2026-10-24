from cutec_ast.node import Node
from cutec_ast.scalar_node import ScalarNode


class ParamNode(Node):
    name: str
    value: ScalarNode|None

    def __init__(self, name: str, value: ScalarNode|None=None):
        self.name = name
        self.value = value
        super().__init__()
