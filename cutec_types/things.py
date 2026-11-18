#
# The CuteC Thing Type
#
from cutec_types.types import Type, BaseType

class ThingType(Type):
    def __init__(
        self,
        parent_type: Type|None = None,
        attribute_types: list[Type]|None = None,
        action_types: list[Type]|None = None
    ):
        super().__init__(BaseType.Thing)
        self.parent_type: Type|None = parent_type

        if attribute_types is None:
            attribute_types = []
        self.attribute_types: list[Type] = attribute_types

        if action_types is None:
            action_types = []
        self.action_types: list[Type] = action_types

    def matches(self, expected_type: Type | None) -> bool:
        if not isinstance(expected_type, ThingType):
            return False

        if self.parent_type:
            return self.parent_type.matches(expected_type)
        else:
            return self == expected_type
