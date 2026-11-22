
from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes
from cutec_types.types import Type


class CatchNode(Node):
    def __init__(self, condition: Node, action: Node):
        self.condition = condition
        self.action = action
        super().__init__()

    def __str__(self) -> str:
        return '(' + str(self.condition) + ') ' + str(self.action)

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        # our condition is handled, we just add our frame bytes
        self.action.add_bytes(bytecode)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        return self.action.get_type(bytecode)