#
# The CuteC Actions Typing System
#
from cutec_types.base_type import BaseType
from cutec_types.types import Type

class ParamType(Type):
    def __init__(
        self,
        param_type: Type,
        required: bool = True
    ):
        super().__init__(BaseType.Action)
        self.param_type = param_type
        self.required = required

    def matches(self, expected_type: Type|None, param_types: list[Type]|None = None) :
        if expected_type is None:
            if self.required:
                raise TypeError('Missing argument for ' + str(self) + ' parameter')
        else:
            self.param_type.matches(expected_type)

    def __str__(self) -> str:
        return str(self.param_type)


class ActionType(Type):
    def __init__(
        self,
        return_type: Type,
        param_types: list[ParamType]|None = None
    ):
        super().__init__(BaseType.Action)

        self.index: int = -1
        self.return_type: Type = return_type
        self.param_types_required = []

        if param_types is None:
            param_types = []

        self.param_types: list[Type] = [p.param_type for p in param_types]
        self.param_types_required = [p.required for p in param_types]

    def matches(self, expected_type: Type|None):
        if not isinstance(expected_type, ActionType):
            raise TypeError('Expected type action, got ' + str(expected_type or 'None'))

        # we don't allow passing extra params
        if len(self.param_types) > len(expected_type.param_types):
            raise TypeError('Expected ' + str(len(expected_type.param_types)) + ', got ' + str(len(self.param_types)))

        # make sure that every expected type is either optional or has a valid passed type
        for ep_index, ep in enumerate(expected_type.param_types):
            if ep_index >= len(self.param_types):
                param_type = None
            else:
                param_type = self.param_types[ep_index]

            # turn ep back into a param type for matching
            ep = ParamType(ep, expected_type.param_types_required[ep_index])
            if not ep.type_check(param_type).passes:
                raise TypeError("Action parameter " + str(ep_index) + " expected " + str(ep.param_type) + ", got " + str(param_type or 'None'))

    def __str__(self) -> str:
        return_type = str(self.return_type)
        param_types = [str(pt) for pt in self.param_types]

        return '(' + ', '.join(param_types) + ') / ' + str(return_type)


