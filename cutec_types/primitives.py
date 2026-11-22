from cutec_types.cutec_type import CutecType
from cutec_types.types import Type, BaseType


class PrimitiveType(Type):
    def __init__(
        self,
        primitive_type: CutecType
    ):
        super().__init__(BaseType.Primitive)
        self.primitive_type: CutecType = primitive_type

    def matches(self, expected_type: Type|None) -> bool:
        if not isinstance(expected_type, PrimitiveType):
            return False

        numeric_conversion_types = [
            CutecType.Bool,
            CutecType.Int,
            CutecType.Dbl,
            CutecType.Char
        ]

        if self.primitive_type == expected_type.primitive_type:
            return True
        else:
            return expected_type.primitive_type in numeric_conversion_types and self.primitive_type in numeric_conversion_types