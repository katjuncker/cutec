from logging import warning

from cutec_ast.node import Node
from cutec_ast.scalar_node import CutecType
from cutec_bytecode.bytes import CutecBytes, CUTEC_NOT


class UnaryOp(Node):
    right: Node
    op: str

    def __init__(self, op: str, right: Node):
        self.op = op
        self.right = right
        super().__init__()

    def __str__(self) -> str:
        return '(' + self.op + ' ' + str(self.right) + ')'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        if self.op == 'not':
            self.right.add_bytes(bytecode)
            bytecode.add_ins(CUTEC_NOT)
        else:
            warning('CuteC compile warning: Invalid unary operator - ' + self.op)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> CutecType:
        return CutecType.Bool