import sys
import struct

OP_LOADC = 4
OP_LOAD  = 1
OP_STORE = 6
OP_ROR   = 3

def parse_asm(path):
    program = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split(';')[0].strip()
            if not line:
                continue
            parts = line.replace(',', ' ').split()
            op = parts[0].upper()

            if op == 'LOADC':
                const, reg = map(int, parts[1:3])
                program.append({'A': OP_LOADC, 'B': const, 'C': reg})

            elif op == 'LOAD':
                reg_dst, reg_ptr = map(int, parts[1:3])
                program.append({'A': OP_LOAD, 'B': reg_dst, 'C': reg_ptr})

            elif op == 'STORE':
                reg_src, reg_ptr, offset = map(int, parts[1:4])
                program.append({'A': OP_STORE, 'B': reg_src, 'C': reg_ptr, 'D': offset})

            elif op == 'ROR':
                reg, mem = map(int, parts[1:3])
                program.append({'A': OP_ROR, 'B': reg, 'C': mem})

            else:
                raise ValueError(f'Unknown instruction: {op}')
    return program

def assemble(program):
    binary = bytearray()
    for ins in program:
        A = ins['A']
        if A == OP_LOADC:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 13)
            binary += struct.pack('<I', word)[0:3]

        elif A == OP_LOAD:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 8)
            binary += struct.pack('<H', word)

        elif A == OP_STORE:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 8) | (ins['D'] << 13)
            binary += struct.pack('<I', word)[0:3]

        elif A == OP_ROR:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 8)
            binary += struct.pack('<I', word)
    return binary

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python main.py asm <source.asm> <output.bin> [test]')
        sys.exit(1)

    mode = sys.argv[1]
    src_file = sys.argv[2]
    out_file = sys.argv[3]
    test_mode = len(sys.argv) > 4 and sys.argv[4] == 'test'

    if mode == 'asm':
        program = parse_asm(src_file)
        if test_mode:
            binary = assemble(program)
            print(' '.join(f'{b:02X}' for b in binary))
        else:
            binary = assemble(program)
            with open(out_file, 'wb') as f:
                f.write(binary)
            print(f"BINARY SIZE: {len(binary)} bytes")