from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_POP


class FrameNode(Node):
    nodes: list[Node]

    def __init__(self, nodes=None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        super().__init__()

    def __str__(self) -> str:
        return '{\n' + ''.join(['\t' + str(n) + '\n' for n in self.nodes]) + '}'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        for node in self.nodes:
            # these are statements so we express them and then pop
            node.add_bytes(bytecode)
            bytecode.add_ins(CUTEC_POP)
        return bytecode
