from cutec_ast.node import Node

class ScalarNode(Node):
    data_type: str
    value: int|float|str

    def __init__(self, data_type: str, value: int|float|str):
        self.data_type = data_type
        self.value = value
        super().__init__()

    def __str__(self) -> str:
        return self.data_type + '(' + str(self.value) + ')'
