from cutec_types.base_type import BaseType
from cutec_types.type_check import TypeCheck

#
# The CuteC General Typing System
#
# This represents any type within the CuteC language.
#
class Type:
    def __init__(
        self,
        base_type: BaseType
    ):
        self.base_type = base_type

    # def get_usage_type(self) -> Type:
    #     if isinstance(self, ActionType):
    #         # when you use a function, it evaluates to the return type
    #         return self.return_type
    #     else:
    #         # everything else (variables, classes, constants, etc.) are just the type
    #         return self


    def matches(self, expected_type: Type|None):
        pass

    def type_check(self, expected_type: Type|None) -> TypeCheck:
        if self.base_type == BaseType.Placeholder or (expected_type and expected_type.base_type == BaseType.Placeholder):
            return TypeCheck(True)

        try:
            self.matches(expected_type)
            return TypeCheck(True)
        except TypeError as e:
            return TypeCheck(False, str(e))

    def __str__(self) -> str:
        return 'type-undefined'