#
# The CuteC Thing Type
#
from cutec_types.types import Type, BaseType

class ThingType(Type):
    def __init__(
        self,
        type_name: str,
        parent_type: Type|None = None,
        attribute_types: list[Type]|None = None,
        action_types: list[Type]|None = None
    ):
        super().__init__(BaseType.Thing)

        self.index: int = -1
        self.type_name = type_name
        self.parent_type: Type|None = parent_type

        if attribute_types is None:
            attribute_types = []
        self.attribute_types: list[Type] = attribute_types

        if action_types is None:
            action_types = []
        self.action_types: list[Type] = action_types

        # specifies whether or not the type definition has been seen or not or if we've just seen a reference to it
        self.complete = len(action_types) > 0 or len(attribute_types) > 0


    def matches(self, expected_type: Type | None) -> bool:
        if not isinstance(expected_type, ThingType):
            return False

        if self.parent_type:
            return self.parent_type.matches(expected_type)
        else:
            return self.type_name == expected_type.type_name

    def __str__(self) -> str:
        return '(thing)'