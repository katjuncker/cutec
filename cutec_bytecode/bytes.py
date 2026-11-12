import struct

from cutec_bytecode.label_maker import LabelMaker

CUTEC_JMP_FALSY_POP = 0b010
CUTEC_JMP           = 0b011
CUTEC_POP           = 0b100
CUTEC_ADD           = 0b101
CUTEC_SUB           = 0b110
CUTEC_MUL           = 0b111
CUTEC_DIV           = 0b1000
CUTEC_MOD           = 0b1001
CUTEC_POW           = 0b1010
CUTEC_SQR           = 0b1011
CUTEC_ABS           = 0b1100
CUTEC_PUSH          = 0b1110
CUTEC_LOAD          = 0b10010
CUTEC_STORE         = 0b10100
CUTEC_JMP_TRUTHY    = 0b10101
CUTEC_JMP_FALSY     = 0b10110
CUTEC_EQ            = 0b10111
CUTEC_GT            = 0b11000
CUTEC_GTE           = 0b11001
CUTEC_LT            = 0b11010
CUTEC_LTE           = 0b11011
CUTEC_NOT           = 0b11100
CUTEC_NEQ           = 0b11101
CUTEC_DATA_STR      = 0b11110

op_codes = {
    CUTEC_JMP: ('jmp', 4),
    CUTEC_ADD: ('add', 0),
    CUTEC_SUB: ('sub', 0),
    CUTEC_MUL: ('mul', 0),
    CUTEC_DIV: ('div', 0),
    CUTEC_MOD: ('mod', 0),
    CUTEC_POW: ('pow', 0),
    CUTEC_POP: ('pop', 0),
    CUTEC_PUSH: ('push', 8),
    CUTEC_LOAD: ('load', 1),
    CUTEC_STORE: ('store', 1),
    CUTEC_JMP_TRUTHY: ('jmp_t', 4),
    CUTEC_JMP_FALSY: ('jmp_f', 4),
    CUTEC_JMP_FALSY_POP: ('jmp_fp', 4),
    CUTEC_EQ: ('eq', 0),
    CUTEC_GT: ('gt', 0),
    CUTEC_LT: ('lt', 0),
    CUTEC_GTE: ('gte', 0),
    CUTEC_LTE: ('lte', 0),
    CUTEC_NOT: ('not', 0),
    CUTEC_NEQ: ('neq', 0),
    CUTEC_DATA_STR: ('data_s', 4)
}


class CutecBytes:
    label_maker = LabelMaker()
    data = []
    actions = []

    def __init__(self):
        self.instructions: list[str] = []
        self.variable_map = {}

    def add(self, ins: str):
        self.instructions.append(ins)

    def add_ins(self, ins: int):
        ins_text = op_codes[ins][0]
        self.add(ins_text)

    def add_ins_wdata(self, ins: int, data):
        ins_text = self.get_ins_text(ins) + ' ' + str(data)
        self.add(ins_text)

    def add_data(self, value) -> int:
        if value in self.data:
            return self.data.index(value)
        self.data.append(value)
        return len(self.data) - 1

    def add_label(self, label: str):
        self.add('')
        self.add(label + ':')

    def make_label(self) -> str:
        return self.label_maker.make()

    def get_ins_text(self, ins: int) -> str:
        return op_codes[ins][0]

    def register_variable(self, name: str):
        if name not in self.variable_map:
            self.variable_map[name] = True
        return name

    def get_variable(self, name: str) -> str:
        if name not in self.variable_map:
            raise ValueError('CuteC: No such variable ' + name)
        return name

    def register_action(self, params, bytecode: CutecBytes) -> int:
        self.actions.append((len(self.actions), params, bytecode))
        return len(self.actions) - 1

    def format_bytes(self, level=0) -> str:
        program = ''
        has_data = len(self.data) > 0
        has_actions = len(self.actions) > 0

        if has_data and level == 0:
            program += '.data\n'
            data_index = 0
            for d in self.data:
                program += '  ' + str(data_index) + ': ' + d + '\n'
                data_index += 1
            program += '\n'

        if has_actions and level == 0:
            program += '.actions\n'
            for action in self.actions:
                program += '  ' + str(action[0]) + ':'
                program += action[2].format_bytes(level + 1) + '\n'
            program += '\n'

        instructions = '\n'.join(self.instructions)
        program += instructions

        # add indents
        program_lines = [(' ' * level * 4) + line for line in program.split('\n')]
        return ('\n'.join(program_lines)).strip('\r\n')

