from enum import StrEnum

from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_DATA


class CutecType (StrEnum):
    Str = 's'
    Int = 'i'
    Char = 'c'
    Dbl = 'd'
    Obj = 'o'
    Bool = 'b'
    Action = 'a'

class ScalarNode(Node):
    data_type: CutecType
    value: int|float|str|bool|None

    def __init__(self, data_type: CutecType, value: int|float|str):
        self.data_type = data_type
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return self.data_type.name + '(' + str(self.value) + ')'

    def get_type(self, bytecode: CutecBytes) -> CutecType:
        return self.data_type

    def format_str(self) -> str:
        str_types = [CutecType.Str, CutecType.Int, CutecType.Dbl, CutecType.Char]

        if self.data_type in str_types:
            if self.data_type == CutecType.Str:
                return repr(self.value)[1:-1]
            return str(self.value)
        elif self.data_type == CutecType.Bool:
            if self.value:
                return 'true'
            else:
                return 'false'
        else:
            raise TypeError('Invalid scalar value of type: ' + self.data_type.name)


    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        str_index = bytecode.add_data(self)
        bytecode.add_ins_wdata(CUTEC_DATA, str_index)
        return bytecode

