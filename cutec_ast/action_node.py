from cutec_ast.node import Node
from cutec_ast.param_node import ParamNode


class ActionNode(Node):
    frame: Node
    params: list[ParamNode]

    def __init__(self, frame: Node, params: list[ParamNode]|None = None):
        if params is None:
            params = []
        self.params = params
        self.frame = frame
        super().__init__()
