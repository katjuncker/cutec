from logging import warning

from cutec_ast.node import Node
from cutec_ast.param_node import ParamNode
from cutec_ast.scalar_node import CutecType
from cutec_bytecode.bytes import CutecBytes, CUTEC_STORE, CUTEC_LOAD_ACTION


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

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        default_params = []
        required_params = []
        for param in self.params:
            if param.value:
                default_params.append(param)
            else:
                required_params.append(param)
                if len(default_params) > 0:
                    warning('CuteC compile warning: Parameter with default value cannot precede parameter without one.')

        action = CutecBytes()
        # register all of the parameters as local variables for the frame
        for index, param in enumerate(self.params):
            action.register_variable(param.name)
            # add a load/store instruction for each default argument
            if param.value:
                # register the constant value
                param.add_bytes(action)

                # store it for the action
                action.add_ins_wdata(CUTEC_STORE, index)

        # now add the method code!
        self.frame.add_bytes(action)

        # register the main method code
        action_index = bytecode.register_action(self.params, action)

        #todo: the () is just so we know it's a method value for printing
        #we can remove this later as the compiler will know from context that if you're
        #calling something that it must be a method value
        bytecode.add_ins_wdata(CUTEC_LOAD_ACTION, str(action_index))

        return bytecode

    def get_type(self, bytecode: CutecBytes) -> CutecType:
        # todo: need to figure out the object/action typing system for complex types
        return CutecType.Action