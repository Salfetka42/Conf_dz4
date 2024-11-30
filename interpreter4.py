import json
import sys


def deserialize_load(byts):
    a = byts[0] & 0b111111
    b = ((byts[0] >> 6) & 0b11) | ((byts[1] & 0b11111111) << 2) | ((byts[2] & 0b11111111) << 10) | (
                (byts[3] & 0b11111111) << 18) | ((byts[4] & 0b111) << 26)
    return a, b


def deserialize_read(byts):
    a = byts[0] & 0b111111
    return a


def deserialize_write(byts):
    A = byts[0] & 0b111111
    B = ((byts[0] >> 6) & 0b11) | ((byts[1] & 0b11111111) << 2) | ((byts[2] & 0b11111111) << 10)| ((byts[3] & 0b1111111) << 18)
    return A, B

def interpret(binary_file, memory_range, output_file):
    memory = [0] * 1024
    with open(binary_file, 'rb') as file:
        binary_data = file.read()
    pc = 0
    accumulator = 0  # Регистр-аккумулято
    A = 0
    B = 0
    while pc < len(binary_data):

        d = binary_data[pc:pc + 5]
        # word = int.from_bytes(d, 'big')
        # A = ((word >> 32) & 0b111111)
        # print(A)
        A = deserialize_read(d)
        if A == 21:  # LOAD_CONST
            A, B = deserialize_load(d)
            # print(A, B)
            accumulator = B
            print(accumulator)
            # print(f"LOAD_CONST: accumulator = {accumulator}")  # Debug

        elif A == 27:  # READ_MEM
            # A = deserialize_read(d)
            # print(accumulator)
            # print(f"READ_MEM: accumulator = memory[{accumulator}]")  # Debug
            accumulator = memory[accumulator]

        elif A == 28:  # WRITE_MEM
            A, B =deserialize_write(d)
            print(A,B)
            # print(f"WRITE_MEM: memory[{B}] = accumulator ({accumulator})")  # Debug
            memory[B] = accumulator

        elif A == 10:  # SGN (Унарная операция)
            A, B = deserialize_load(d)
            if accumulator > 0:
                result = 1
            elif accumulator < 0:
                result = -1
            else:
                result = 0
            memory[B] = result
            print(f"SGN: memory[{B}] = {result} (from accumulator={accumulator})")  # Debug
        pc += 5  # Переход к следующей команде


    # Печать состояния памяти перед сохранением
    print(f"Final memory state: {memory[memory_range[0]:memory_range[1]]}")

    # Формирование результата
    result = {"memory_range": memory_range, "values": memory[memory_range[0]:memory_range[1]]}

    # Сохранение результата в файл
    with open(output_file, 'w') as result_file:
        json.dump(result, result_file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python interpreter4.py <input.bin> <start:end> <output.json> [expected_memory.json]")
        sys.exit(1)

    binary_file = sys.argv[1]
    memory_range = list(map(int, sys.argv[2].split(':')))
    output_file = sys.argv[3]
    interpret(binary_file, memory_range, output_file)

# python interpreter4.py output4.bin 0:1000 result4.json
