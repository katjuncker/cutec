from enum import StrEnum


class BaseType (StrEnum):
    Primitive = 'p'
    Action = 'a'
    Thing = 't'

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


    def matches(self, expected_type: Type|None) -> bool:
        return False

    def __str__(self) -> str:
        return 'type-undefined'

    def is_primitive(self):
        return False