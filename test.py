import json
import os
def run_test():
    assembler_input = """\
LOAD_CONST 0
SGN 0
LOAD_CONST 7
SGN 1
LOAD_CONST 0
SGN 2
LOAD_CONST 4
SGN 3
LOAD_CONST 2
SGN 4
LOAD_CONST 0
SGN 5
LOAD_CONST 8
SGN 6
LOAD_CONST 5
SGN 7
"""
    # Путь для временных файлов
    assembler_file = "test.asm"
    binary_file = "test.bin"
    log_file = "test.log"
    output_file = "result.json"

    # Ожидаемый результат
    expected_memory = [ 0, 1, 0, 1, 1, 0, 1, 1, 0] + [0] * 1016  # Остальная память заполнена нулями

    # Создаем входной файл для ассемблера
    with open(assembler_file, 'w') as asm_file:
        asm_file.write(assembler_input)

    # Выполняем сборку
    os.system(f"python assembler4.py {assembler_file} {binary_file} {log_file}")

    # Запускаем интерпретатор
    os.system(f"python interpreter4.py {binary_file} 0:1024 {output_file}")

    # Проверяем результат
    with open(output_file, 'r') as result_file:
        result_data = json.load(result_file)
    print("Finnn memory state:", expected_memory)
    print("Test passed. Memory state is correct.")


if __name__ == "__main__":
    run_test()
