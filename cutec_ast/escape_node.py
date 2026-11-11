from cutec_ast.frame_node import FrameNode
from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes


class EscapeNode(Node):
    timeout: Node
    action: FrameNode

    def __init__(self, timeout: Node, action: FrameNode):
        self.timeout = timeout
        self.action = action
        super().__init__()

    def __str__(self) -> str:
        return 'escape (' + str(self.timeout) + ')' + ' {\n'+ str(self.action) + '}'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.action.add_bytes(bytecode)
        return bytecode
