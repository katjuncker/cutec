import struct
from logging import warning

from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_PUSH


class ScalarNode(Node):
    data_type: str
    value: int|float|str

    def __init__(self, data_type: str, value: int|float|str):
        self.data_type = data_type
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return self.data_type + '(' + str(self.value) + ')'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        if self.data_type == 'number':
            bytecode.add_ins_wdata(CUTEC_PUSH, str(self.value))
        else:
            warning(
                'CuteC compile warning: ' + self.__class__.__name__ + ' does not implement the ' + self.data_type + ' data type.')

        return bytecode

