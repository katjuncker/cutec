from cutec_bytecode.bytes import CutecBytes
from cutec_parser import CutecParser

cutec = CutecParser()

print('CuteC> ', end=None)
lines = []
while True:
    line = input('')
    if line == "GO.":
        break
    lines.append(line)

program = '\n'.join(lines)
ast = cutec.parse(program)

if ast:
    # print(ast)
    bytecode = CutecBytes()
    ast.add_bytes(bytecode)
    print(bytecode.format_bytes())
