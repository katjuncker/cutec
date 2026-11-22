from logging import warning

from cutec_ast.node import Node
from cutec_ast.param_node import ParamNode
from cutec_bytecode.bytes import CutecBytes, CUTEC_STORE, CUTEC_LOAD_ACTION
from cutec_types.actions import ActionType
from cutec_types.placeholder_type import PlaceholderType
from cutec_types.type_system import TypeSystem
from cutec_types.types import Type


class ActionNode(Node):

    def __init__(self, frame: Node, params: list[ParamNode]|None = None, return_type: Type|None = None):
        if params is None:
            params = []
        self.params: list[ParamNode] = params
        self.frame = frame
        self.return_type = return_type
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

        action = CutecBytes(TypeSystem())
        self.get_type(action)

        # register all of the parameters as local variables for the frame

        # this gives the 'self' variable index 0 while allowing the interpreter to specially assign it
        params = self.params.copy()
        params.insert(0, ParamNode('self', PlaceholderType()))

        for index, param in enumerate(params):
            action.register_variable(param.name, param.value)
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

    def get_type(self, bytecode: CutecBytes) -> Type:
        # register the special self type
        bytecode.type_system.register_variable('self', PlaceholderType())

        # register our params with the type system
        for index, param in enumerate(self.params):
            param_type = param.get_type(bytecode)
            bytecode.type_system.register_variable(param.name, param_type.param_type)

        # get the type of the action body
        declared_return_type = self.return_type
        actual_return_type = self.frame.get_type(bytecode)

        if isinstance(actual_return_type, PlaceholderType):
            raise TypeError('Action is purely recursive with no escape.')

        if declared_return_type and not actual_return_type.type_check(declared_return_type).passes:
            raise TypeError('Actual return value of ' + str(actual_return_type) + ' does not match declared type of ' + str(declared_return_type))

        return_type = declared_return_type or actual_return_type

        param_types = []
        for param in self.params:
            param_types.append(param.get_type(bytecode))

        action_type = bytecode.type_system.register_action(ActionType(return_type, param_types))

        # re-register it now that we know what it really is
        bytecode.type_system.register_variable('self', action_type)

        # now check the body of the method again (should always be safe)
        self.frame.get_type(bytecode)

        return action_type