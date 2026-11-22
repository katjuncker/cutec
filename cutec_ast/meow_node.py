from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_MEOW
from cutec_types.types import Type


class MeowNode(Node):
    def __init__(self, value: Node):
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return '( meow ' + str(self.value) + ' )'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.value.add_bytes(bytecode)
        bytecode.add_ins(CUTEC_MEOW)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        return self.value.get_type(bytecode)