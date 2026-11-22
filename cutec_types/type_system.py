from cutec_types.actions import ActionType, ParamType
from cutec_types.primitives import PrimitiveType
from cutec_types.things import ThingType
from cutec_types.types import Type

class TypeSystem:
    # all of the things we've seen
    things: list[ThingType] = []

    # all of the actions we might take
    actions: list[ActionType] = []

    # a mapping of thing names to their corresponding thing indexes
    # this is here because they're global and we're trying to move type info away from CutecBytes
    # kind of a bad design choice there really :(
    things_map: dict[str, int] = {}

    def __init__(self):
        # keeps tracks of variables in this frame
        self.variables: list[Type] = []
        self.variables_map: dict[str, int] = {}

        # keeps tracks of all possible returns during this frame
        self.return_types: list[Type] = []

    def register_thing(self, thing_type: ThingType) -> ThingType:
        """
        This creates an index for any kind of thing.
        The thing might be anonymous or at least not have a name yet, so we just want to keep track of it's index for later tracking and bytecode generation.

        :param thing_type:
        :return:
        """
        thing_type.index = len(self.things)
        self.things.append(thing_type)
        return thing_type

    def assign_thing_name(self, index: int, name: str):
        """
        Once we've seen the name for a thing, i.e. in the thing declaration node,
        we can take the type's index and assign it's name.

        :param index:
        :param name:
        :return:
        """
        if len(self.things) <= index:
            raise TypeError('Attempted to assign name to unregistered type ' + str(index))
        self.things_map[name] = index

    def register_type(self, name: str) -> ThingType:
        """
        Lets the type system know about a type that we haven't seen the definition for yet.
        This gives it a stable index and lets the system know to expect it later (or flip out about not seeing it)

        :param name:
        :return:
        """
        if name in self.things_map:
            return self.things[self.things_map[name]]
        else:
            thing_type = self.register_thing(ThingType(name))
            self.assign_thing_name(thing_type.index, name)
            return thing_type


    def register_action(self, action_type: ActionType) -> ActionType:
        action_type.index = len(self.actions)
        self.actions.append(action_type)
        return action_type

    def register_variable(self, name: str, data_type: Type) -> Type:
        if name in self.variables_map:
            expected_type = self.variables[self.variables_map[name]]
            if not data_type.matches(expected_type):
                raise TypeError('Attempted to assign a value of type ' + str(data_type) + ' to variable ' + name + ' of type ' + str(expected_type))
            return data_type

        self.variables_map[name] = len(self.variables)
        self.variables.append(data_type)
        return data_type

    def get_variable_index(self, name: str) -> int:
        if name not in self.variables_map:
            raise TypeError('Reference to undeclared variable ' + name)
        return self.variables_map[name]

    def get_variable_type_by_name(self, name: str) -> Type:
        return self.variables[self.get_variable_index(name)]

    def get_variable_type_by_index(self, index: int) -> Type:
        if index not in self.variables:
            raise TypeError('Reference to undeclared variable ' + str(index))
        return self.variables[index]

    def add_return_type(self, return_type: Type):
        self.return_types.append(return_type)

    def get_shared_type(self, types: list[Type]) -> Type:
        """
        Takes a list of types and finds the closest shared type that all types match.
        For example, if you had a Cat and a Dog, you'd return Animal as you can guarantee that both values are an Animal and not call any methods that might not be present or indexable.

        If this is a method, we find a shared type for the return and each parameter.
        That's insanely complicated, but CuteC is amazing.

        If a common type cannot be found, an exception is thrown.

        Note: You cannot safely convert between floats/ints as the compiler may use special instructions for either and would have to cast the return value to the widest data type.
        We may do this in the future, but for now, the programmer must do that themselves.

        :param types:
        :return:
        """
        if len(types) < 1:
            raise ValueError('Must be passed at least one type.')

        shared_type = types.pop()
        while len(types) != 0:
            next_type = types.pop()
            shared_type = self.__find_shared(shared_type, next_type)
        return shared_type

    def __find_shared(self, t1: Type, t2: Type) -> Type:
        if isinstance(t1, PrimitiveType) and isinstance(t2, PrimitiveType):
            if t1.primitive_type == t2.primitive_type:
                return t1

        if isinstance(t1, ThingType) and isinstance(t2, ThingType):
            # find a nearest common parent
            if t1.type_name == t2.type_name:
                return t1

            if t1.matches(t2) and t1.parent_type:
                return self.__find_shared(t1.parent_type, t2)
            elif t2.matches(t1) and t2.parent_type:
                return self.__find_shared(t2.parent_type, t1)
            else:
                raise TypeError('Mixed usage of things ' + t1.type_name + ' and ' + t2.type_name)

        if isinstance(t1, ActionType) and isinstance(t2, ActionType):
            # find lots of shared types and do stuff
            shared_return_type = self.__find_shared(t1.return_type, t2.return_type)

            if len(t1.param_types) != len(t2.param_types):
                raise TypeError('Mixed usage of actions with different parameter counts.')

            shared_param_types = []
            for index, p1 in enumerate(t1.param_types):
                p2 = t2.param_types[index]
                shared_param_types.append(self.__find_shared(p1, p2))

            return ActionType(shared_return_type, shared_param_types)

        if isinstance(t1, ParamType) and isinstance(t2, ParamType):
            # find lots of shared types and do stuff
            if t1.required != t2.required:
                raise TypeError('Mixed usage of required and unrequired parameters.')
            return self.__find_shared(t1.param_type, t2.param_type)

        raise TypeError('No shared type found among t1, t2')

type_system = TypeSystem()