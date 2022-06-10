import re
from bitarray import bitarray


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


def read_registers() -> dict:
    registers = dict()

    for line in open("registers.txt", 'r').readlines():
        line = line[:-1].split(';')
        registers[line[0]] = line[1]

    return registers


def dec_to_bin(dec_value: str, size: int) -> str:
    dec_value_int = int(dec_value)

    if dec_value_int < 0:
        if dec_value_int < -2 ** (size - 1):
            raise ValueError("Valor imediato menor do que o tamanho suportado.")
        else:
            bin_value = format(dec_value_int, f"0{size + 1}b")[1:].replace("1", "x").replace("0", "1").replace("x", "0")
            neg_bin = ""
            changed = False
            for bit in bin_value[::-1]:
                if not changed:
                    if bit == "1":
                        neg_bin += "0"
                    else:
                        neg_bin += "1"
                        changed = True
                else:
                    neg_bin += bit
            return neg_bin[::-1]
    elif dec_value_int >= 2 ** size:
        raise ValueError("Valor imediato maior do que o tamanho suportado.")
    else:
        return format(dec_value_int, f"0{size}b")


class Instruction:
    type_dict, opcode_dict, function_dict = read_instructions()
    register_dict = read_registers()

    def __init__(self, name: str, instruction_list: list, has_label_start: bool, has_label_final: bool, pos: int,
                 labels: dict):
        self.name = name
        self.opcode = Instruction.opcode_dict[name]
        self.type = Instruction.type_dict[name]
        self.has_immediate = False
        self.has_label_start = has_label_start
        self.has_label_final = has_label_final
        # tratando os registradores
        if self.type != "j":
            if has_label_start:
                offset = 1
            else:
                offset = 0
            if self.name == "jr":
                self.rs = Instruction.register_dict[instruction_list[1 + offset]]
                self.rt = dec_to_bin("0", 5)
                self.rd = dec_to_bin("0", 5)
            elif self.type == "r":
                if name != "sll" and name != "srl":
                    self.rd = Instruction.register_dict[instruction_list[1 + offset]]
                    self.rs = Instruction.register_dict[instruction_list[2 + offset]]
                    self.rt = Instruction.register_dict[instruction_list[3 + offset]]
                else:
                    self.rs = Instruction.register_dict[instruction_list[1 + offset]]
                    self.rt = dec_to_bin("0", 5)
                    self.rd = Instruction.register_dict[instruction_list[2 + offset]]
            elif self.type == "i":
                if name == 'lw' or name == 'sw':
                    rs = instruction_list[-1]
                    rs = rs.split("(")[1].replace(")", '')
                    self.rs = Instruction.register_dict[rs]
                else:
                    self.rs = Instruction.register_dict[instruction_list[2 + offset]]
                if has_label_final:
                    self.immediate = dec_to_bin(str(labels[instruction_list[-1]] - pos - 1), 16)
                self.rt = Instruction.register_dict[instruction_list[1 + offset]]
        else:
            if has_label_final:
                self.immediate = dec_to_bin(str(labels[instruction_list[-1]]), 26)
        # function and shamt sem tratar o label no final
        if self.type == "r":
            self.function = Instruction.function_dict[name]
            if name == 'sll' or name == "srl":
                self.has_immediate = True
                self.shamt = dec_to_bin(instruction_list[-1], 5)
            else:
                self.shamt = dec_to_bin('0', 5)
        if (self.type == "i" or self.type == "j") and not self.has_label_final:
            immediate = instruction_list[-1]
            if name == "lw" or name == "sw":
                immediate = immediate.split("(")[0]
                self.immediate = dec_to_bin(immediate, 16)
            self.immediate = dec_to_bin(immediate, 16)

    def info(self):
        print(f'Nome = {self.name}')
        print(f'Opcode = {self.opcode}')
        print(f'Tipo = {self.type}')

        if self.type != "j" and not self.has_label_start:
            print(f'RS = {self.rs}')
            if self.name != 'jr':
                print(f'RT {self.rt}')
                if self.type == "r":
                    print(f'RD {self.rd}')

        if self.type == "r":
            print(f'Shamt = {self.shamt}')
            print(f'Function {self.function}')
        if self.type == "i" or self.type == "j":
            print(f'Endereço/imediato = {self.immediate}')
        print()


def read_asm() -> list:
    pattern = r"[ ,]"
    instruction_list = list()
    try:
        file = open("entrada.asm", "r")
    except FileNotFoundError:
        file = open("exemplo.asm", "r")
    for line in file.readlines():
        line = re.split(pattern, line.replace("\n", "").lower())
        for i in range(line.count("")):
            line.remove("")
        instruction_list.append(line)
    return instruction_list


def create_labels(list_instruction: list[str]) -> dict:
    labels = dict()
    for i, instruction in enumerate(list_instruction):
        if ":" in instruction[0]:
            labels[instruction[0].replace(":", "")] = i

    return labels


def check_instruction(list_instruction: list, pos: int, labels: dict):
    last_word_instruction = list_instruction[-1]
    has_label_init = False
    has_label_final = False

    if ":" in list_instruction[0]:
        has_label_init = True
    if last_word_instruction.isalpha():
        has_label_final = True

    if not has_label_init:
        instruction_obj = Instruction(list_instruction[0], list_instruction, has_label_init, has_label_final, pos,
                                      labels)
    else:
        instruction_obj = Instruction(list_instruction[1], list_instruction, has_label_init, has_label_final, pos,
                                      labels)

    if instruction_obj.type == 'i':
        instruction_obj.has_immediate = True

    return instruction_obj


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')


def file_write(instruction: str, file):
    for i in instruction:
        i = bitstring_to_bytes(i)
        file.write(i)


def transforming_instruction(list_instruction: list, labels: dict):
    with open("saida.bin", "wb") as file:
        output = bitarray(32*len(list_instruction))
        for i, l in enumerate(list_instruction):
            instruction_obj = check_instruction(l, i, labels)
            # instruction_obj.info()

            if instruction_obj.type == "r":
                instruction = instruction_obj.opcode + instruction_obj.rs + instruction_obj.rt + instruction_obj.rd + instruction_obj.shamt + instruction_obj.function
            elif instruction_obj.type == "i":
                instruction = instruction_obj.opcode + instruction_obj.rs + instruction_obj.rt + instruction_obj.immediate
            else:
                instruction = instruction_obj.opcode + instruction_obj.immediate
            for j, byte in enumerate(instruction):
                output[i*32 + j] = int(byte)
        output.tofile(file)


def to_read():
    with open("saida.bin", "rb") as file:
        byte = file.read(4)
        while byte:
            print(format(int.from_bytes(byte, byteorder="little"), f"032b"))
            byte = file.read(4)
