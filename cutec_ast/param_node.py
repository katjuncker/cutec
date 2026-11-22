from cutec_ast.node import Node
from cutec_ast.scalar_node import ScalarNode
from cutec_bytecode.bytes import CutecBytes
from cutec_types.actions import ParamType
from cutec_types.types import Type

class ParamNode(Node):
    def __init__(self, name: str, data_type: Type, value: ScalarNode|None=None):
        self.name = name
        self.data_type = data_type
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        if self.value:
            return self.name + '=' + str(self.value)
        else:
            return self.name

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.get_type(bytecode)  # todo: testing

        if self.value:
            return self.value.add_bytes(bytecode)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        return ParamType(self.data_type, not self.value)