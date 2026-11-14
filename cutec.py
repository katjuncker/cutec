from cutec_bytecode.bytes import CutecBytes
from cutec_bytecode.packer import CutecPacker
from cutec_parser import CutecParser

cutec = CutecParser()

# print('CuteC> ', end=None)
# lines = []
# while True:
#     line = input('')
#     if line == "GO.":
#         break
#     lines.append(line)
#
# program = '\n'.join(lines)

program = """
{ 
  hello = "Hello ";
  world = "world";

  str_cmp = action (s1, s2 = "") -> chase(
    s1 > s2 -> s1,
    s2 > s1 -> s2,
    escape -> 0
  );
  
  y = str_cmp(hello, "world");
  y;
}
"""

ast = cutec.parse(program)

if ast:
    # print(ast)
    bytecode = CutecBytes()
    ast.add_bytes(bytecode)
    print(bytecode.format_program())
    print('----------')

    packer = CutecPacker()
    packed = bytecode.pack_program(packer)
    print('---Packed---')
    print(packed)
    with open('program.cutec', 'wb') as packed_file:
        packed_file.write(packed)


