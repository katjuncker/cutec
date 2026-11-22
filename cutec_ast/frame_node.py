from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_POP
from cutec_types.types import Type


class FrameNode(Node):
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

    def get_type(self, bytecode: CutecBytes) -> Type:
        return_types = bytecode.type_system.return_types
        if len(return_types) > 0:
            return bytecode.type_system.get_shared_type(return_types)
        else:
            return self.nodes[-1].get_type(bytecode)
