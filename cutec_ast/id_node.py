from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_LOAD


class IdNode(Node):
    name: str

    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def __str__(self) -> str:
        return self.name

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        name = bytecode.get_variable(self.name)
        bytecode.add_ins_wdata(CUTEC_LOAD, name)
        return bytecode




