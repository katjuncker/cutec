from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_STORE
from cutec_types.types import Type


class DeclareNode(Node):
    def __init__(self, name: str, data_type: Type|None, value: Node|None = None):
        if not data_type and not value:
            raise ValueError('A variable declaration requires either a type or a value.')

        self.name = name
        self.value = value
        self.data_type = data_type

        super().__init__()

    def __str__(self) -> str:
            type_name = self.data_type if self.data_type is not None else '(inferred)'
            value = self.value if self.value is not None else '(default)'
            return self.name + '/' + type_name + ' = ' + str(value)

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        # we aren't going to register variables unless they have a value
        # the type system will still know about them and not have any issues with them
        # but this prevents us from generating bytecode for a variable that has never been assigned a value
        if self.value:
            name = bytecode.register_variable(self.name, None)
            self.value.add_bytes(bytecode)
            bytecode.add_ins_wdata(CUTEC_STORE, name)

        return bytecode

    def get_type(self, bytecode: CutecBytes) -> Type:
        data_type = None

        if self.data_type:
            data_type = bytecode.type_system.register_variable(self.name, self.data_type)

        if self.value:
            value_type = self.value.get_type(bytecode)
            data_type = data_type or value_type

            # registering again will do nothing except check the types
            bytecode.type_system.register_variable(self.name, value_type)

        if data_type is None:
            raise TypeError('No data type for declaration: this cannot happen.')

        return data_type

