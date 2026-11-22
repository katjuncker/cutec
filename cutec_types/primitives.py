from cutec_types.base_type import BaseType
from cutec_types.cutec_type import CutecType
from cutec_types.types import Type


class PrimitiveType(Type):
    def __init__(
        self,
        primitive_type: CutecType
    ):
        super().__init__(BaseType.Primitive)
        self.primitive_type: CutecType = primitive_type

    def matches(self, expected_type: Type|None):
        if not isinstance(expected_type, PrimitiveType):
            raise TypeError('Expected primitive type, got ' + str(expected_type or 'None'))

        numeric_conversion_types = [
            CutecType.Bool,
            CutecType.Int,
            CutecType.Dbl,
            CutecType.Char
        ]

        if self.primitive_type == expected_type.primitive_type:
            return None
        else:
            valid_conversion = expected_type.primitive_type in numeric_conversion_types and self.primitive_type in numeric_conversion_types

            if not valid_conversion:
                raise TypeError('Invalid primitive conversion between ' + self.primitive_type + ' and ' + expected_type.primitive_type)
            return None

    def __str__(self) -> str:
        return self.primitive_type.name