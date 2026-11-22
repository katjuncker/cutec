from cutec_types.base_type import BaseType
from cutec_types.type_check import TypeCheck
from cutec_types.types import Type

class PlaceholderType(Type):
    def __init__(
        self
    ):
        super().__init__(BaseType.Placeholder)

    def matches(self, expected_type: Type|None):
        return None

    def type_check(self, expected_type: Type|None) -> TypeCheck:
        return TypeCheck(True)

    def __str__(self) -> str:
        raise TypeError('Cannot use placeholder type.')