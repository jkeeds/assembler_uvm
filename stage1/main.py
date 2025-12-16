import sys
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
            for i, ins in enumerate(program):
                print(f"{i}: {ins}")
        else:
            import pickle
            with open(out_file, 'wb') as f:
                pickle.dump(program, f)
    else:
        print('Unknown mode')
