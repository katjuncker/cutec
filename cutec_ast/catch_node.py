from cutec_ast.frame_node import FrameNode
from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes


class CatchNode(Node):
    condition: Node
    action: Node

    def __init__(self, condition: Node, action: Node):
        self.condition = condition
        self.action = action
        super().__init__()

    def __str__(self) -> str:
        return '(' + str(self.condition) + ') ' + str(self.action)

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        # our condition is handled, we just add our frame bytes
        self.action.add_bytes(bytecode)
        return bytecode