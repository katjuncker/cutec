from cutec_ast.node import Node
from cutec_ast.scalar_node import CutecType
from cutec_bytecode.bytes import CutecBytes, CUTEC_LOAD


class IdNode(Node):
    name: str

    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def __str__(self) -> str:
        return self.name

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        name, data_type, value = bytecode.get_variable(self.name)
        bytecode.add_ins_wdata(CUTEC_LOAD, name)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> CutecType:
        name, data_type, value = bytecode.get_variable(self.name)
        return data_type




