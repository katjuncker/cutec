from cutec_ast.catch_node import CatchNode
from cutec_ast.escape_node import EscapeNode
from cutec_ast.node import Node
from cutec_ast.scalar_node import CutecType
from cutec_bytecode.bytes import CutecBytes, CUTEC_JMP_FALSY, CUTEC_JMP, CUTEC_JMP_FALSY_POP, CUTEC_PUSH


class ChaseNode(Node):
    catches: list[CatchNode]
    escape: EscapeNode|None

    def __init__(self, catches: list[CatchNode], escape: EscapeNode|None = None):
        self.catches = catches
        self.escape = escape
        super().__init__()

    def __str__(self) -> str:
        catches_str = ''.join(['\t' + str(c) + '\n' for c in self.catches])
        if self.escape:
            return 'chase\n' + catches_str + str(self.escape)
        else:
            return 'chase\n' + catches_str

    def add_bytes(self, bytecode: CutecBytes) -> CutecBytes:
        label = bytecode.make_label()
        label_end = label + '_end'
        label_escape = label + '_escape'

        # since a chase is an expression, it needs to produce a null/none if no condition matches and no escape is provided
        label_none_end = label + '_none'

        catch_index = 1
        for catch in self.catches:
            last_catch = catch_index == len(self.catches)
            first_catch = catch_index == 1

            if last_catch:
                if self.escape:
                    label_next = label_escape
                else:
                    label_next = label_none_end
            else:
                label_next = label + '_catch_' + str(catch_index + 1)

            # if we're not the first catch we'll add a numbered label so the prevoius thing can jump to us
            if not first_catch:
                bytecode.add_label(label + '_catch_' + str(catch_index))

            # evaluate the condition
            catch.condition.add_bytes(bytecode)

            # if it's falsy we jump to the next catch label/escape/end
            bytecode.add_ins_wdata(CUTEC_JMP_FALSY_POP, label_next)

            # now we add all of the actionable bytecode and a jump to the end
            catch.add_bytes(bytecode)
            bytecode.add_ins_wdata(CUTEC_JMP, label_end)

            catch_index += 1

        # if there's an escape, we need to let you jump to it
        if self.escape:
            bytecode.add_label(label_escape)
            self.escape.add_bytes(bytecode)
            bytecode.add_ins_wdata(CUTEC_JMP, label_end)

        # add none end label if there is a chance there is no value
        if not self.escape:
            bytecode.add_label(label_none_end)
            bytecode.add_ins_wdata(CUTEC_PUSH, 'None')

        # add the end label
        bytecode.add_label(label_end)

        return bytecode

    def get_type(self, bytecode: CutecBytes) -> CutecType:
        data_type = self.catches[0].get_type(bytecode)

        values: list[Node] = self.catches.copy()
        if self.escape:
            values.append(self.escape)

        for v in values:
            t = v.get_type(bytecode)
            if t != data_type:
                raise TypeError('All catches and escapes must return ' + data_type.name + ' - found ' + t.name)

        return data_type