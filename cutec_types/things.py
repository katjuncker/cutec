#
# The CuteC Thing Type
#
from cutec_types.base_type import BaseType
from cutec_types.types import Type

class ThingType(Type):
    def __init__(
        self,
        type_name: str,
        parent_type: ThingType|None = None,
        attribute_types: list[Type]|None = None,
        action_types: list[Type]|None = None
    ):
        super().__init__(BaseType.Thing)

        self.index: int = -1
        self.type_name = type_name
        self.parent_type: ThingType|None = parent_type

        if attribute_types is None:
            attribute_types = []
        self.attribute_types: list[Type] = attribute_types

        if action_types is None:
            action_types = []
        self.action_types: list[Type] = action_types

        # specifies whether or not the type definition has been seen or not or if we've just seen a reference to it
        self.complete = len(action_types) > 0 or len(attribute_types) > 0


    def matches(self, expected_type: Type | None):
        if not isinstance(expected_type, ThingType):
            raise TypeError('Expected a thing, got ' + str(expected_type or 'None'))

        self_type = self
        while self_type is not None:
            if self_type.type_name == expected_type.type_name:
                return None
            else:
                self_type = self_type.parent_type

        raise TypeError('Expected thing of type ' + str(expected_type) + ', got ' + str(self))

    def __str__(self) -> str:
        return '(thing)'