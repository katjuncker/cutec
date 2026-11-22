from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from cutec_bytecode.cutec_compile_error import CuteCompileError
from cutec_bytecode.bytes import CUTEC_STORE, CUTEC_LOAD, CUTEC_PUSH, CUTEC_DATA, CUTEC_LOAD_ACTION, \
        CUTEC_CALL, CUTEC_JMP_TRUTHY, CUTEC_JMP_FALSY, CUTEC_JMP, CUTEC_JMP_FALSY_POP, op_codes
from cutec_types.cutec_type import CutecType

if TYPE_CHECKING:
    from cutec_bytecode.bytes import CutecBytes

class CutecPacker:
    def __init__(self):
        self.labels_map = {}
        self.label_count = 0

    def pack(self, program: str, bytecode: CutecBytes) -> bytes:
        # first thing in a program is data
        data, program = self.read_data(program, bytecode)

        # read the actions
        actions, program = self.read_actions(program, bytecode)

        # read the entry point
        cutec = self.read_cutec(program, bytecode)

        if not cutec:
            raise CuteCompileError('no executable code was provided')

        # now it's time to pack everything!
        packed = self.pack_data(data)
        packed.extend(self.pack_actions(actions))

        # write the entry code / header length
        cutec_ins = self.pack_instructions(cutec)
        packed.extend(len(cutec_ins).to_bytes(4, 'big', signed=False))
        packed.extend(cutec_ins)

        return bytes(packed)

    def read_data(self, program: str, bytecode: CutecBytes):
        data = []
        start_str = '.data:'
        if not program.startswith(start_str):
            return None, program

        # Consume '.data:'
        program = program[len(start_str):]

        # Consume any remaining newlines
        program = program.lstrip('\r\n')

        while True:
            # Check for indent
            if not program.startswith('  '):
                break

            # Consume indent
            program = program[2:]

            index_part, sep, program = program.partition(': ')
            if not sep:
                break

            data_index = int(index_part)
            type_str, _, program = program.partition(',')
            data_value, _, program = program.partition('\n')
            data_value = data_value.rstrip('\r')

            data.append((data_index, type_str, data_value))

        return data, program.lstrip('\r\n')

    def read_actions(self, program, bytecode):
        actions = []
        start_str = '.actions:'
        if not program.startswith(start_str):
            return None, program

        # Consume '.data:'
        program = program[len(start_str):]

        # Consume any remaining newlines
        program = program.lstrip('\r\n')

        while True:
            # Check for indent
            if not program.startswith('  '):
                break

            # read the action index
            action_line, _, program = program.partition('\n')
            program = program.lstrip('\r')

            # consume indent and trailing :
            action_line = action_line[2:-1]
            action_index, param_len, param_len_required = [int(part) for part in action_line.split(',')]

            # now just parse every line that begins with 4 spaces
            lines = program.split('\n')
            instructions = []
            for line in lines:
                if not line.startswith('    '):
                    break

                # consume the line from the program
                program = program[len(line + '\n'):]
                instructions.append(line.strip())

            actions.append((action_index, param_len, param_len_required, instructions))

        return actions, program.lstrip('\r\n')

    def read_cutec(self, program, bytecode):
        start_str = '.cutec:'
        if not program.startswith(start_str):
            return None

        # Consume '.cutec:'
        program = program[len(start_str):]
        lines = program.split('\n')
        return [line.strip() for line in lines]

    def pack_data(self, data) -> bytearray:
        data_bytes = bytearray(b'.data')
        data_len = len(data)
        data_bytes.extend(data_len.to_bytes(4, 'big', signed=False))

        for d in data:
            d_index = int(d[0])
            d_type = d[1]
            d_value = d[2]

            data_bytes.extend(d_index.to_bytes(4, 'big', signed=False))

            if d_type == CutecType.Str:
                data_bytes.extend(b's')
                # str_value = d_value.encode('utf-8')
                str_value = d_value.encode('utf-8').decode('unicode_escape').encode('utf-8')
                d_len = len(str_value)
                data_bytes.extend(d_len.to_bytes(4, 'big', signed=False))
                data_bytes.extend(str_value)
            elif d_type == CutecType.Int:
                data_bytes.extend(b'i')
                d_value = int(d_value)
                data_bytes.extend(d_value.to_bytes(4, 'big', signed=True))
            elif d_type == CutecType.Dbl:
                data_bytes.extend(b'd')
                d_value = float(d_value)
                data_bytes.extend(struct.pack('>d', d_value))
            elif d_type == CutecType.Bool:
                data_bytes.extend(b'b')
                if d_value == 'true':
                    data_bytes.extend(b't')
                else:
                    data_bytes.extend(b'f')
            elif d_type == CutecType.Char:
                data_bytes.extend(b'c')
                data_bytes.append(ord(d_value[0]))
            else:
                raise ValueError('CuteC Packer: invalid type ' + d_type)

        return data_bytes

    def pack_actions(self, actions) -> bytearray:
        data_bytes = bytearray(b'.actions')

        data_len = len(actions)
        data_bytes.extend(data_len.to_bytes(4, 'big', signed=False))

        for action in actions:
            action_index = int(action[0])
            data_bytes.extend(action_index.to_bytes(4, 'big', signed=False))

            param_len = int(action[1])
            data_bytes.extend(param_len.to_bytes(1, 'big', signed=False))

            param_len_required = int(action[2])
            data_bytes.extend(param_len_required.to_bytes(1, 'big', signed=False))

            ins_bytes = self.pack_instructions(action[3], True)
            data_bytes.extend(len(ins_bytes).to_bytes(4, 'big', signed=False))
            data_bytes.extend(ins_bytes)

        return data_bytes

    def pack_instructions(self, instructions: list[str], in_action = False) -> bytearray:
        # we need to leave 4 bytes to write the length at the end
        data_bytes = bytearray()
        labels = {}
        unresolved_jumps = []
        byte_index = 0



        # in actions, we reserve 0 for self (eventually we'll add this too)
        variable_count = 0 if not in_action else 1
        variable_map = {} if not in_action else {
            'self': 0
        }

        op_code_map = {}
        for op_code in op_codes:
            op_code_map[op_codes[op_code][0]] = op_code

        line_no = 0
        for ins in instructions:
            line_no += 1
            ins = ins.strip()
            if ins == '':
                continue

            is_label = ins.endswith(':')
            ins, has_data, data = ins.partition(' ')

            if is_label:
                label_name = ins[:-1]
                labels[label_name] = byte_index
                continue
            else:
                op_code = op_code_map[ins]
                data_len = op_codes[op_code][1]

                if data_len > 0 and not has_data:
                    raise CuteCompileError('instruction ' + ins + ' requires a data value but none was provided [at line ' + str(line_no) + ']')
                if data_len == 0 and has_data:
                    raise CuteCompileError(
                        'instruction ' + ins + ' was provided unnecessary data [at line ' + str(line_no) + ']')

                # encode the instruction
                data_bytes.extend(op_code.to_bytes(1, 'big', signed=False))
                byte_index += 1

                # encode the data with special cases
                var_ops = [CUTEC_STORE, CUTEC_LOAD]
                byte_ops = [CUTEC_CALL]
                int_ops = [CUTEC_DATA, CUTEC_LOAD_ACTION]
                jmp_ops = [CUTEC_JMP, CUTEC_JMP_FALSY_POP, CUTEC_JMP_TRUTHY, CUTEC_JMP_FALSY]

                if op_code in var_ops:
                    # get the variable index

                    if data not in variable_map:
                        if variable_count > 255:
                            raise CuteCompileError(
                                'Variable ' + data + ' exceeds the 255 variable limit per frame [at line ' + str(line_no) + ']')
                        variable_map[data] = variable_count
                        variable_count += 1

                    data_bytes.extend(variable_map[data].to_bytes(1, 'big', signed=False))

                elif op_code == CUTEC_PUSH:
                    # this is always a float though it might technically handle
                    # floats, ints, chars, nulls, and True/False values via nan-boxing
                    # and/or context
                    data_bytes.extend(struct.pack('>d', float(data)))

                elif op_code in byte_ops:
                    data_bytes.extend(int(data).to_bytes(1, 'big', signed=False))

                elif op_code in int_ops:
                    data_bytes.extend(int(data).to_bytes(4, 'big', signed=False))

                elif op_code in jmp_ops:
                    if data in labels:
                        # add the byte index for this label
                        data_bytes.extend(labels[data].to_bytes(4, 'big', signed=False))
                    else:
                        # we haven't seen this label yet so we'll store it's position
                        # and we'll overwrite it in the bytecode later
                        unresolved_jumps.append((data, byte_index, line_no))
                        data_bytes.extend(int(0).to_bytes(4, 'big', signed=False))

                byte_index += data_len

        # now we should have all of the unresolved jump labels
        for jump, byte_index, line_no in unresolved_jumps:
            if jump not in labels:
                raise CuteCompileError(
                    'Could not resolve jump for ' + jump + ' [at line ' + str(line_no) + ']')
            else:
                # overwrite the bytecode
                label_index = labels[jump]
                data_bytes[byte_index:byte_index + 4] = label_index.to_bytes(
                    4, 'big', signed=False
                )

        return data_bytes



