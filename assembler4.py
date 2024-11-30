import json
import struct
import sys


def serialize_load(A, B):
    bytes_array = [0] * 5
    bytes_array[0] = (A & 0b111111) | ((B & 0b11) << 6)  # A в 0-5 биты, B в 6-7
    bytes_array[1] = (B >> 2) & 0b11111111                     # B: 8-15 биты
    bytes_array[2] = (B >> 10) & 0b11111111                 # B: 16-23 биты
    bytes_array[3] = (B >> 18) & 0b11111111                  # B: 24-31 биты
    bytes_array[4] = (B >> 26) & 0b111              # B: 32-34 биты
    return bytes(bytes_array)


def deserialize_load(byts):
    A = byts[0] & 0b111111
    B = ((byts[0] >> 6) & 0b11) | ((byts[1] & 0b11111111) << 2) | ((byts[2] & 0b11111111) << 10) | ((byts[3] & 0b11111111) << 18) | ((byts[4] & 0b111) << 26)
    return A, B

def serialize_read(A):
    bytes_array = [0] * 5
    bytes_array[0] = (A & 0b111111)
    return bytes(bytes_array)

def deserialize_read(byts):
    A = byts[0] & 0b111111
    return A


def serialize_write(A, B):
    bytes_array = [0] * 5
    bytes_array[0] = (A & 0b111111) | ((B & 0b11) << 6)  # A в 0-5 биты, B в 6-7
    bytes_array[1] = (B >> 2) & 0b11111111                    # B: 8-15 биты
    bytes_array[2] = (B >> 10) & 0b11111111                    # B: 16-23 биты
    bytes_array[3] = (B >> 18) & 0b1111111                  # B: 24-31 биты
    return bytes(bytes_array)

def deserialize_write(byts):
    A = byts[0] & 0b111111
    B = ((byts[0] >> 6) & 0b11) | ((byts[1] & 0b1111111) << 10) | ((byts[2] & 0b11111111) << 18)
    return A, B

def assemble(input_file, output_bin, log_file):
    commands = {
        "LOAD_CONST": 21,
        "READ_MEM": 27,
        "WRITE_MEM": 28,
        "SGN": 10
    }
    binary_data = []
    log_data = []

    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            cmd = parts[0]
            print(parts[0],parts[1])
            if cmd == "LOAD_CONST":
                A = commands[cmd]
                B = int(parts[1])  # Поле B — константа
                print(A, B)
                print(deserialize_load(serialize_load(A,B)))
                binary_data.append(serialize_load(A, B))
                log_data.append({
                    "command": cmd,
                    "A": A,
                    "B": B,
                    "bytes": serialize_load(A, B).hex()
                })



            elif cmd == "READ_MEM":
                A = commands[cmd]
                binary_data.append(serialize_read(A))
                print(A)
                print(deserialize_load(serialize_read(A)))
                log_data.append({
                    "command": cmd,
                    "A": A,
                    "bytes": serialize_read(A).hex()
                })

            elif cmd == "WRITE_MEM":
                A = commands[cmd]
                B = int(parts[1])  # Поле B — адрес для записи
                print(A, B)
                print(deserialize_load(serialize_write(A, B)))
                binary_data.append(serialize_write(A, B))
                log_data.append({
                    "command": cmd,
                    "A": A,
                    "B": B,
                    "bytes": serialize_write(A, B).hex()
                })


            elif cmd == "SGN":
                A = commands[cmd]
                B = int(parts[1])  # Поле B — адрес для записи результата
                print(B)
                print(deserialize_load(serialize_write(A, B)))
                binary_data.append(serialize_write(A, B))
                log_data.append({
                    "command": cmd,
                    "A": A,
                    "B": B,
                    "bytes": serialize_write(A, B).hex()
                })


    # Save binary data
    with open(output_bin, 'wb') as bin_file:
        for data in binary_data:
            bin_file.write(data)

    # Save log data
    with open(log_file, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler4.py <input.asm> <output4.bin> <log4.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_bin = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_bin, log_file)
#python assembler4.py test4.asm output4.bin log4.json
# "f02840ee00"
# "8030200d00"
# "902360ee80"
# "b03260a1b7"