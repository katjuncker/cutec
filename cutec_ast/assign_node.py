from logging import warning

from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_STORE
from cutec_types.types import Type


class AssignNode(Node):
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
        self.get_type(bytecode)  # todo: testing

        if self.obj:
            warning('CuteC compile warning: Object assigment not implemented')
        name = bytecode.register_variable(self.name, self.value)
        self.value.add_bytes(bytecode)
        bytecode.add_ins_wdata(CUTEC_STORE, name)

        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        data_type = self.value.get_type(bytecode)

        # if we haven't seen the variable before, we'll register it
        # otherwise, we'll do nothing except verify that the value type is OK
        return bytecode.type_system.register_variable(self.name, data_type)