from cutec_ast.frame_node import FrameNode
from cutec_ast.node import Node
from cutec_ast.scalar_node import CutecType
from cutec_bytecode.bytes import CutecBytes


class EscapeNode(Node):
    timeout: Node
    value: Node

    def __init__(self, timeout: Node, value: Node):
        self.timeout = timeout
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return 'escape (' + str(self.timeout) + ')' + ' {\n'+ str(self.action) + '}'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.value.add_bytes(bytecode)
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> CutecType:
        return self.value.get_type(bytecode)
