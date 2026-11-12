from cutec_ast.node import Node
from cutec_ast.scalar_node import ScalarNode
from cutec_bytecode.bytes import CutecBytes


class ParamNode(Node):
    name: str
    value: ScalarNode|None

    def __init__(self, name: str, value: ScalarNode|None=None):
        self.name = name
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        if self.value:
            return self.name + '=' + str(self.value)
        else:
            return self.name

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        if self.value:
            return self.value.add_bytes(bytecode)
        return bytecode