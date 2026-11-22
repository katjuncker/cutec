from cutec_bytecode.bytes import CutecBytes
from cutec_bytecode.packer import CutecPacker
from cutec_parser import CutecParser
import subprocess

from cutec_types.type_system import TypeSystem, type_system

cutec = CutecParser()

program = """
meow meow
{ 
  say_hi = action () -> 0;

  x/int = 0;
  meow x;
}
"""

ast = cutec.parse(program)

if ast:
    bytecode = CutecBytes(type_system)
    ast.add_bytes(bytecode)

    with open('program.cutec', 'w', encoding='utf-8') as cutec_file:
        cutec_file.write(bytecode.format_program())

    packer = CutecPacker()
    packed = bytecode.pack_program(packer)

    with open('program.casm', 'wb') as packed_file:
        packed_file.write(packed)

    # execute the program
    cutec_cmd = ['CuteC.exe', 'program.casm']
    result = subprocess.run(cutec_cmd, capture_output=True, text=True)

    print("Exit Code: " + str(result.returncode))
    print("Output:\n" + result.stdout)
    if result.stderr:
        print("Errors:\n" + result.stderr)


