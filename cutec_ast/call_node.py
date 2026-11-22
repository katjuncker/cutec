from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_CALL
from cutec_bytecode.cutec_compile_error import CuteCompileError
from cutec_types.actions import ActionType, ParamType
from cutec_types.placeholder_type import PlaceholderType
from cutec_types.types import Type


class CallNode(Node):
    def __init__(self, action: Node, arguments: list[Node]|None = None):
        self.action = action
        if arguments is None:
            arguments = []
        self.arguments = arguments

        if len(arguments) > 255:
            raise CuteCompileError('action cannot have more than 255 arguments')

        super().__init__()

    def __str__(self) -> str:
        arg_str = ', '.join([str(arg) for arg in self.arguments])
        return '( ' + str(self.action) + '(' + arg_str + ')' + ' )'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.get_type(bytecode)  # todo: testing

        # push the action part to the stack
        self.action.add_bytes(bytecode)

        for arg in self.arguments:
            # push each argument
            arg.add_bytes(bytecode)

        # call it!
        bytecode.add_ins_wdata(CUTEC_CALL, str(len(self.arguments)))
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        # we're going to need to pass things like this
        expected_type = self.action.get_type(bytecode)

        # this might be self() or something we don't know about
        if isinstance(expected_type, PlaceholderType):
            return expected_type

        if not isinstance(expected_type, ActionType):
            raise TypeError('Attempting to call non-action type.')

        # the type that this expression evaluates to
        return_type = expected_type.return_type

        # build a pseudo ActionType to ensure that our types match
        # this has to return the return_type so we just use it
        argument_types = [ParamType(arg.get_type(bytecode)) for arg in self.arguments]
        action_type = ActionType(return_type, argument_types)

        # this raises an exception so we know exactly what failed
        type_check = expected_type.type_check(action_type)
        if not type_check.passes:
            raise TypeError(type_check.error)

        return expected_type.return_type