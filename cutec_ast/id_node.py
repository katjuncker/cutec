from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_LOAD
from cutec_types.types import Type


class IdNode(Node):
    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def __str__(self) -> str:
        return self.name

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.get_type(bytecode)  # todo: testing

        name, value = bytecode.get_variable(self.name)
        bytecode.add_ins_wdata(CUTEC_LOAD, name)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        return bytecode.type_system.get_variable_type_by_name(self.name)




