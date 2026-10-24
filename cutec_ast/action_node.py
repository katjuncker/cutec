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

    def __str__(self) -> str:
        param_str = ', '.join([str(p) for p in self.params])
        frame_str = str(self.frame)
        return f"""( action ({param_str}) {{
{frame_str}
}} )
"""

