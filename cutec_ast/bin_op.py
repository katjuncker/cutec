from logging import warning

from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_ADD, CUTEC_SUB, CUTEC_MUL, CUTEC_DIV, CUTEC_MOD, CUTEC_POW, CUTEC_EQ, \
    CUTEC_NEQ, CUTEC_GT, CUTEC_LT, CUTEC_GTE, CUTEC_LTE, CUTEC_NOT, CUTEC_JMP_TRUTHY, CUTEC_POP, CUTEC_JMP_FALSY


class BinOp(Node):
    left: Node
    right: Node
    op: str

    def __init__(self, op: str, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right
        super().__init__()

    def __str__(self) -> str:
        return '(' + str(self.left) + ' ' + self.op + ' ' + str(self.right) + ')'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        bin_op_map = {
            '+': CUTEC_ADD,
            '-': CUTEC_SUB,
            '*': CUTEC_MUL,
            '/': CUTEC_DIV,
            '%': CUTEC_MOD,
            '^': CUTEC_POW,
            '==': CUTEC_EQ,
            '!=': CUTEC_NEQ,
            '>': CUTEC_GT,
            '<': CUTEC_LT,
            '>=': CUTEC_GTE,
            '<=': CUTEC_LTE,
        }

        logical_ops = ['or', 'and']

        if self.op in bin_op_map:
            self.left.add_bytes(bytecode)
            self.right.add_bytes(bytecode)
            bytecode.add_ins(bin_op_map[self.op])
        elif self.op in logical_ops:
            if self.op == 'or':
                label = bytecode.make_label() + '_or_end'

                # evaluate the LHS
                self.left.add_bytes(bytecode)

                # now we need to skip to the end if true
                bytecode.add_ins_wdata(CUTEC_JMP_TRUTHY, label)

                # evaluate the right hand side
                bytecode.add_ins(CUTEC_POP)
                self.right.add_bytes(bytecode)

                # add the label at the end
                bytecode.add_label(label)

                pass
            elif self.op == 'and':
                label = bytecode.make_label() + '_and_end'

                # evaluate the LHS
                self.left.add_bytes(bytecode)

                # now we need to skip to the end if false
                bytecode.add_ins_wdata(CUTEC_JMP_FALSY, label)

                # evaluate the right hand side
                bytecode.add_ins(CUTEC_POP)
                self.right.add_bytes(bytecode)

                # add the label at the end
                bytecode.add_label(label)
                pass
        else:
            warning('CuteC compile warning: ' + self.__class__.__name__ + ' does not implement the ' + self.op + ' operator.')

        return bytecode



