from logging import warning

from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_STORE


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

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        if self.obj:
            warning('CuteC compile warning: Object assigment not implemented')

        name = bytecode.register_variable(self.name)
        self.value.add_bytes(bytecode)
        bytecode.add_ins_wdata(CUTEC_STORE, name)

        return bytecode