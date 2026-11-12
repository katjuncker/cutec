from logging import warning

from cutec_ast.node import Node
from cutec_ast.param_node import ParamNode
from cutec_bytecode.bytes import CutecBytes, CUTEC_PUSH, CUTEC_STORE, CUTEC_JMP

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
        for param in self.params:
            action.register_variable(param.name)

        # we need a label to handle each possible parameter count variation
        for param_count in range(len(required_params), len(self.params) + 1):
            action.add_label('method_params_' + str(param_count))

            # todo: handle this via a standard bytecode class and maybe merge them?
            # for every parameter passed, we'll store the pushed values from calling
            # these must be pushed in reverse order
            for param_index in reversed(range(0, param_count)):
                action.add_ins_wdata(CUTEC_STORE, self.params[param_index].name)

            # now we need to push/store all of the default values if any are remaining
            if param_count < len(self.params):
                #e.g. if this is for when you pass 2 params but 3 are needed (1 default)
                # this means that we only need to handle the 3rd default value
                defaults = default_params[len(self.params) - param_count - 1:]
                for default_param in defaults:
                    default_param.value.add_bytes(action)
                    action.add_ins_wdata(CUTEC_STORE, default_param.name)

            # jump to the start of the method
            action.add_ins_wdata(CUTEC_JMP, 'method_start')

        # now add the method code!
        action.add_label('method_start')
        self.frame.add_bytes(action)

        # register the main method code
        action_index = bytecode.register_action(self.params, action)

        #todo: the () is just so we know it's a method value for printing
        #we can remove this later as the compiler will know from context that if you're
        #calling something that it must be a method value
        bytecode.add_ins_wdata(CUTEC_PUSH, str(action_index) + '()')

        return bytecode

