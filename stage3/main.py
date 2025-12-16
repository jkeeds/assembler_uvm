import sys
import struct
import csv
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
                B, C = map(int, parts[1:3])
                program.append({'A': OP_LOADC, 'B': B, 'C': C})

            elif op == 'LOAD':
                B, C = map(int, parts[1:3])
                program.append({'A': OP_LOAD, 'B': B, 'C': C})

            elif op == 'STORE':
                B, C, D = map(int, parts[1:4])
                program.append({'A': OP_STORE, 'B': B, 'C': C, 'D': D})

            elif op == 'ROR':
                B, C = map(int, parts[1:3])
                program.append({'A': OP_ROR, 'B': B, 'C': C})

            else:
                raise ValueError(f'Unknown instruction: {op}')
    return program


def assemble(program):
    binary = bytearray()
    for ins in program:
        A = ins['A']

        if A == OP_LOADC:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 13)
            binary += struct.pack('<I', word)[:3]

        elif A == OP_LOAD:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 8)
            binary += struct.pack('<H', word)

        elif A == OP_STORE:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 8) | (ins['D'] << 13)
            binary += struct.pack('<I', word)[:3]

        elif A == OP_ROR:
            word = (A & 0x7) | (ins['B'] << 3) | (ins['C'] << 8)
            binary += struct.pack('<I', word)

    return binary

def ror(val, n):
    n %= 32
    return ((val >> n) | (val << (32 - n))) & 0xFFFFFFFF

def interpret(bin_path, dump_path, mem_range):
    regs = [0] * 32
    data_mem = [0] * 2048
    with open(bin_path, 'rb') as f:
        code = f.read()
    ip = 0
    while ip < len(code):
        A = code[ip] & 0x7
        if A == OP_LOADC:
            word = struct.unpack('<I', code[ip:ip+3] + b'\x00')[0]
            B = (word >> 3) & 0x3FF
            C = (word >> 13) & 0x1F
            regs[C] = B
            ip += 3
        elif A == OP_LOAD:
            word = struct.unpack('<H', code[ip:ip+2])[0]
            B = (word >> 3) & 0x1F
            C = (word >> 8) & 0x1F
            regs[B] = data_mem[regs[C]]
            ip += 2
        elif A == OP_STORE:
            word = struct.unpack('<I', code[ip:ip+3] + b'\x00')[0]
            B = (word >> 3) & 0x1F
            C = (word >> 8) & 0x1F
            D = (word >> 13) & 0x3FF
            data_mem[regs[C] + D] = regs[B]
            ip += 3
        elif A == OP_ROR:
            word = struct.unpack('<I', code[ip:ip+4])[0]
            B = (word >> 3) & 0x1F
            C = (word >> 8) & 0xFFFFF
            regs[B] = ror(regs[B], data_mem[C])
            ip += 4
        else:
            raise RuntimeError('Invalid opcode')
    start, end = map(int, mem_range.split(':'))
    with open(dump_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['address', 'value'])
        for i in range(start, end):
            writer.writerow([i, data_mem[i]])

if __name__ == '__main__':
    if sys.argv[1] == 'asm':
        program = parse_asm(sys.argv[2])
        binary = assemble(program)
        with open(sys.argv[3], 'wb') as f:
            f.write(binary)
        print(len(binary))

    elif sys.argv[1] == 'run':
        interpret(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        print('Usage:')
        print('  uvm.py asm program.asm program.bin')
        print('  uvm.py run program.bin dump.csv start:end')
