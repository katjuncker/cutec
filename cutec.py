from cutec_bytecode.bytes import CutecBytes
from cutec_bytecode.packer import CutecPacker
from cutec_parser import CutecParser
import subprocess

cutec = CutecParser()

program = """
meow meow
{ 
  meow "Hello, world!\n";

  recursive_add = action (n, self) -> chase(
    n <= 0 -> 0,
    escape -> n + self(n - 1, self)
  );
  
  meow recursive_add(1000, recursive_add);
}
"""

ast = cutec.parse(program)

if ast:
    bytecode = CutecBytes()
    ast.add_bytes(bytecode)

    packer = CutecPacker()
    packed = bytecode.pack_program(packer)

    with open('program.cutec', 'w', encoding='utf-8') as cutec_file:
        cutec_file.write(bytecode.format_program())

    with open('program.casm', 'wb') as packed_file:
        packed_file.write(packed)

    # execute the program
    cutec_cmd = ['CuteC.exe', 'program.casm']
    result = subprocess.run(cutec_cmd, capture_output=True, text=True)

    print("Exit Code: " + str(result.returncode))
    print("Output:\n" + result.stdout)
    if result.stderr:
        print("Errors:\n" + result.stderr)


