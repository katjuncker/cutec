from logging import warning, PlaceHolder

from cutec_ast.node import Node
from cutec_bytecode.bytes import CutecBytes, CUTEC_ADD, CUTEC_SUB, CUTEC_MUL, CUTEC_DIV, CUTEC_MOD, CUTEC_POW, CUTEC_EQ, \
    CUTEC_NEQ, CUTEC_GT, CUTEC_LT, CUTEC_GTE, CUTEC_LTE, CUTEC_JMP_TRUTHY, CUTEC_POP, CUTEC_JMP_FALSY
from cutec_types.cutec_type import CutecType
from cutec_types.placeholder_type import PlaceholderType
from cutec_types.primitives import PrimitiveType
from cutec_types.types import Type


class BinOp(Node):
    def __init__(self, op: str, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right
        super().__init__()

    def __str__(self) -> str:
        return '(' + str(self.left) + ' ' + self.op + ' ' + str(self.right) + ')'

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        self.get_type(bytecode)  # todo: testing

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

    def get_type(self, bytecode: CutecBytes) -> Type:
        left_type = self.left.get_type(bytecode)
        right_type = self.right.get_type(bytecode)

        math_ops = ['+', '-', '*', '/', '%', '^']
        logic_ops = ['==', '!=', '>', '<', '>=', '<=', 'and', 'or']

        math_op_map = {
            '+': {
                (CutecType.Dbl, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Int): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Char): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Bool): CutecType.Dbl,

                (CutecType.Int, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Int, CutecType.Int): CutecType.Int,
                (CutecType.Int, CutecType.Char): CutecType.Int,
                (CutecType.Int, CutecType.Bool): CutecType.Int,
                (CutecType.Int, CutecType.Str): CutecType.Str,

                (CutecType.Char, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Char, CutecType.Int): CutecType.Char,
                (CutecType.Char, CutecType.Char): CutecType.Char,
                (CutecType.Char, CutecType.Bool): CutecType.Char,
                (CutecType.Char, CutecType.Str): CutecType.Str,

                (CutecType.Bool, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Bool, CutecType.Int): CutecType.Int,
                (CutecType.Bool, CutecType.Char): CutecType.Char,
                (CutecType.Bool, CutecType.Bool): CutecType.Int,

                (CutecType.Str, CutecType.Int): CutecType.Str,
                (CutecType.Str, CutecType.Char): CutecType.Str,
                (CutecType.Str, CutecType.Str): CutecType.Str,
            },

            '-': {
                (CutecType.Dbl, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Int): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Char): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Bool): CutecType.Dbl,

                (CutecType.Int, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Int, CutecType.Int): CutecType.Int,
                (CutecType.Int, CutecType.Char): CutecType.Int,
                (CutecType.Int, CutecType.Bool): CutecType.Int,
                (CutecType.Int, CutecType.Str): CutecType.Str,

                (CutecType.Char, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Char, CutecType.Int): CutecType.Char,
                (CutecType.Char, CutecType.Char): CutecType.Char,
                (CutecType.Char, CutecType.Bool): CutecType.Char,

                (CutecType.Bool, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Bool, CutecType.Int): CutecType.Int,
                (CutecType.Bool, CutecType.Char): CutecType.Char,
                (CutecType.Bool, CutecType.Bool): CutecType.Int,

                (CutecType.Str, CutecType.Int): CutecType.Str,
                (CutecType.Str, CutecType.Char): CutecType.Str,
                (CutecType.Str, CutecType.Str): CutecType.Str,
            },

            '*': {
                (CutecType.Dbl, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Int): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Char): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Bool): CutecType.Dbl,

                (CutecType.Int, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Int, CutecType.Int): CutecType.Int,
                (CutecType.Int, CutecType.Char): CutecType.Int,
                (CutecType.Int, CutecType.Bool): CutecType.Int,
                (CutecType.Int, CutecType.Str): CutecType.Str,

                (CutecType.Char, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Char, CutecType.Int): CutecType.Char,
                (CutecType.Char, CutecType.Char): CutecType.Char,
                (CutecType.Char, CutecType.Bool): CutecType.Char,
                (CutecType.Char, CutecType.Str): CutecType.Str,

                (CutecType.Bool, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Bool, CutecType.Int): CutecType.Int,
                (CutecType.Bool, CutecType.Char): CutecType.Char,
                (CutecType.Bool, CutecType.Bool): CutecType.Int,

                (CutecType.Str, CutecType.Int): CutecType.Str,
                (CutecType.Str, CutecType.Bool): CutecType.Str
            },

            '/': {
                (CutecType.Dbl, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Int): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Char): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Bool): CutecType.Dbl,

                (CutecType.Int, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Int, CutecType.Int): CutecType.Int,
                (CutecType.Int, CutecType.Char): CutecType.Int,
                (CutecType.Int, CutecType.Bool): CutecType.Int,

                (CutecType.Char, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Char, CutecType.Int): CutecType.Char,
                (CutecType.Char, CutecType.Char): CutecType.Char,
                (CutecType.Char, CutecType.Bool): CutecType.Char,

                (CutecType.Bool, CutecType.Dbl): CutecType.Dbl,
                (CutecType.Bool, CutecType.Int): CutecType.Int,
                (CutecType.Bool, CutecType.Char): CutecType.Int,
                (CutecType.Bool, CutecType.Bool): CutecType.Int,

                (CutecType.Str, CutecType.Int): CutecType.Str,
                (CutecType.Str, CutecType.Char): CutecType.Str,
                (CutecType.Str, CutecType.Str): CutecType.Str
            },

            '%': {
                (CutecType.Dbl, CutecType.Int): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Char): CutecType.Dbl,

                (CutecType.Int, CutecType.Int): CutecType.Int,
                (CutecType.Int, CutecType.Char): CutecType.Int,

                (CutecType.Char, CutecType.Int): CutecType.Char,
                (CutecType.Char, CutecType.Char): CutecType.Char,

                (CutecType.Str, CutecType.Int): CutecType.Str,
                (CutecType.Str, CutecType.Char): CutecType.Str,
                (CutecType.Str, CutecType.Str): CutecType.Str
            },

            '^': {
                (CutecType.Dbl, CutecType.Int): CutecType.Dbl,
                (CutecType.Dbl, CutecType.Char): CutecType.Dbl,

                (CutecType.Int, CutecType.Int): CutecType.Int,
                (CutecType.Int, CutecType.Char): CutecType.Int,

                (CutecType.Char, CutecType.Int): CutecType.Char,
                (CutecType.Char, CutecType.Char): CutecType.Char,

                (CutecType.Bool, CutecType.Dbl): CutecType.Int,
                (CutecType.Bool, CutecType.Int): CutecType.Int,
                (CutecType.Bool, CutecType.Char): CutecType.Int,
                (CutecType.Bool, CutecType.Bool): CutecType.Int
            }
        }

        if self.op in logic_ops:
            # you're all OK.
            return PrimitiveType(CutecType.Bool)
        elif self.op in math_ops:
            # any operation on a placeholder type must be a placeholder type
            # the above boolean logic is fine because we know it has to be boolean
            if isinstance(left_type, PlaceholderType) or isinstance(right_type, PlaceholderType):
                return PlaceholderType()

            if not isinstance(left_type, PrimitiveType):
                raise TypeError('Use of non-primitive type with operator ' + self.op)
            if not isinstance(right_type, PrimitiveType):
                raise TypeError('Use of non-primitive type with operator ' + self.op)

            op_map = math_op_map[self.op]
            key = (left_type.primitive_type, right_type.primitive_type)
            if key not in op_map:
                raise TypeError('Operator ' + self.op + ' is not defined for types ' + left_type.primitive_type.name + ' and ' + right_type.primitive_type.name)
            return PrimitiveType(op_map[key])
        else:
            raise TypeError('Operator ' + self.op + ' is not supported.')



