from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_RETURN
from cutec_types.types import Type


class ReturnNode(Node):
    value: Node

    def __init__(self, value: Node):
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return 'return ' + str(self.value)

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.value.add_bytes(bytecode)
        bytecode.add_ins(CUTEC_RETURN)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        value_type = self.value.get_type(bytecode)
        bytecode.type_system.add_return_type(value_type)
        return value_type