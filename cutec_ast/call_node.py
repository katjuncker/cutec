from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_CALL
from cutec_bytecode.cutec_compile_error import CuteCompileError
from cutec_types.actions import ActionType
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
        # push the action part to the stack
        self.action.add_bytes(bytecode)

        for arg in self.arguments:
            # push each argument
            arg.add_bytes(bytecode)

        # call it!
        bytecode.add_ins_wdata(CUTEC_CALL, str(len(self.arguments)))
        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        action_type = self.action.get_type(bytecode)
        if not isinstance(action_type, ActionType):
            raise TypeError('Attempting to call non-action type.')

        return action_type.return_type