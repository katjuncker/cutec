from cutec_ast.declare_node import DeclareNode
from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes
from cutec_types.actions import ActionType
from cutec_types.things import ThingType
from cutec_types.types import Type


class ThingNode(Node):
    def __init__(self, parent_type: str|None, attributes: list[DeclareNode]):
        self.parent_type = parent_type
        self.attributes = attributes
        super().__init__()

    def __str__(self) -> str:
        return '(thing)'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.get_type(bytecode)  # todo: testing

        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        pt = None
        if self.parent_type:
            # let CuteC know that this type exists (we may not know what it is yet)
            pt = bytecode.type_system.register_type(self.parent_type)

        all_types = [attr.get_type(bytecode) for attr in self.attributes]
        action_types = [t for t in all_types if isinstance(t, ActionType)]
        attribute_types = [t for t in all_types if not isinstance(t, ActionType)]

        return bytecode.type_system.register_thing(ThingType('[unknown]', pt, attribute_types, action_types))