def dec_to_bin(dec_value: str, size: int) -> str:
    if int(dec_value) < 0:
        raise ValueError("Valor imediato negativo.")
    elif int(dec_value) >= 2 ** size:
        raise ValueError("Valor imediato maior do que o tamanho suportado.")
    else:
        bin_value = bin(int(dec_value))[2:]
        return "0" * (size - len(bin_value)) + bin_value


def read_instructions() -> tuple:
    types = dict()
    opcodes = dict()
    functions = dict()
    for line in open("instructions.txt", 'r').readlines():
        line = line[:-1].split(';')
        types[line[0]] = line[1]
        opcodes[line[0]] = line[2]
        if line[1] == 'r':
            functions[line[0]] = line[3]
    return types, opcodes, functions


class Instruction:
    type_dict, opcode_dict, function_dict = read_instructions()

    def __init__(self, name: str):
        self.opcode = Instruction.opcode_dict[name]
