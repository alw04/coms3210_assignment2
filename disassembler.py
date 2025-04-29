import argparse

# define a dictionary of opcodes
# define a nested dictionary for each opcode detailing information about the instruction and it's type
opcodes = {
    0b10001011000: {"instruction": "ADD", "type": "R"},
    0b1001000100: {"instruction": "ADDI", "type": "I"},
    # 0b1011000100: {"instruction": "ADDIS", "type": "I"},
    # 0b10101011000: {"instruction": "ADDS", "type": "R"},
    0b10001010000: {"instruction": "AND", "type": "R"},
    0b1001001000: {"instruction": "ANDI", "type": "I"},
    # 0b1111001000: {"instruction": "ANDIS", "type": "I"},
    # 0b1110101000: {"instruction": "ANDS", "type": "R"},
    0b000101: {"instruction": "B", "type": "B"},
    0b100101: {"instruction": "BL", "type": "B"},
    0b11010110000: {"instruction": "BR", "type": "R"},
    0b10110101: {"instruction": "CBNZ", "type": "CB"},
    0b10110100: {"instruction": "CBZ", "type": "CB"},
    0b01010100: {"instruction": "B.cond", "type": "CB"},  # not sure why this wasn't included in opcodes.txt
    0b11111111110: {"instruction": "DUMP", "type": "R"},
    0b11001010000: {"instruction": "EOR", "type": "R"},
    0b1101001000: {"instruction": "EORI", "type": "I"},
    # 0b00011110011: {"instruction": "FADDD", "type": "R"},
    # 0b00011110001: {"instruction": "FADDS", "type": "R"},
    # 0b00011110011: {"instruction": "FCMPD", "type": "R"},
    # 0b00011110001: {"instruction": "FCMPS", "type": "R"},
    # 0b00011110011: {"instruction": "FDIVD", "type": "R"},
    # 0b00011110001: {"instruction": "FDIVS", "type": "R"},
    # 0b00011110011: {"instruction": "FMULD", "type": "R"},
    # 0b00011110001: {"instruction": "FMULS", "type": "R"},
    # 0b00011110011: {"instruction": "FSUBD", "type": "R"},
    # 0b00011110001: {"instruction": "FSUBS", "type": "R"},
    0b11111111111: {"instruction": "HALT", "type": "R"},
    0b11111000010: {"instruction": "LDUR", "type": "D"},
    # 0b00111000010: {"instruction": "LDURB", "type": "D"},
    # 0b11111100010: {"instruction": "LDURD", "type": "R"},
    # 0b01111000010: {"instruction": "LDURH", "type": "D"},
    # 0b10111100010: {"instruction": "LDURS", "type": "R"},
    # 0b10111000100: {"instruction": "LDURSW", "type": "D"},
    0b11010011011: {"instruction": "LSL", "type": "R"},
    0b11010011010: {"instruction": "LSR", "type": "R"},
    0b10011011000: {"instruction": "MUL", "type": "R"},
    0b10101010000: {"instruction": "ORR", "type": "R"},
    0b1011001000: {"instruction": "ORRI", "type": "I"},
    0b11111111100: {"instruction": "PRNL", "type": "R"},
    0b11111111101: {"instruction": "PRNT", "type": "R"},
    # 0b10011010110: {"instruction": "SDIV", "type": "R"},
    # 0b10011011010: {"instruction": "SMULH", "type": "R"},
    0b11111000000: {"instruction": "STUR", "type": "D"},
    # 0b00111000000: {"instruction": "STURB", "type": "D"},
    # 0b11111100000: {"instruction": "STURD", "type": "R"},
    # 0b01111000000: {"instruction": "STURH", "type": "D"},
    # 0b10111100000: {"instruction": "STURS", "type": "R"},
    # 0b10111000000: {"instruction": "STURSW", "type": "D"},
    0b11001011000: {"instruction": "SUB", "type": "R"},
    0b1101000100: {"instruction": "SUBI", "type": "I"},
    0b1111000100: {"instruction": "SUBIS", "type": "I"},
    0b11101011000: {"instruction": "SUBS", "type": "R"},
    # 0b10011010110: {"instruction": "UDIV", "type": "R"},
    # 0b10011011110: {"instruction": "UMULH", "type": "R"},
}

# for B.cond
condition_codes = {
    0x0: "EQ",
    0x1: "NE",
    0x2: "HS",
    0x3: "LO",
    0x4: "MI",
    0x5: "PL",
    0x6: "VS",
    0x7: "VC",
    0x8: "HI",
    0x9: "LS",
    0xA: "GE",
    0xB: "LT",
    0xC: "GT",
    0xD: "LE",
}


def to_twos_complement(value, bits):
    if value & (1 << (bits - 1)) != 0:
        value = value - (1 << bits)
    return value


def decode_r_type(instruction):
    rm = instruction >> 16 & 0x1F
    shamt = instruction >> 10 & 0x3F
    rn = instruction >> 5 & 0x1F
    rd = instruction & 0x1F
    return {"rm": rm, "shamt": shamt, "rn": rn, "rd": rd}


def decode_i_type(instruction):
    immediate = instruction >> 10 & 0xFFF
    immediate = to_twos_complement(immediate, 12)
    rn = instruction >> 5 & 0x1F
    rd = instruction & 0x1F
    return {"immediate": immediate, "rn": rn, "rd": rd}


def decode_d_type(instruction):
    address = instruction >> 12 & 0x1FF
    address = to_twos_complement(address, 9)
    rn = instruction >> 5 & 0x1F
    rt = instruction & 0x1F
    return {"address": address, "rn": rn, "rt": rt}


def decode_b_type(instruction):
    address = instruction & 0x3FFFFFF
    address = to_twos_complement(address, 26)
    return {"address": address}


def decode_cb_type(instruction):
    address = instruction >> 5 & 0x7FFFF
    address = to_twos_complement(address, 19)
    rt = instruction & 0x1F
    return {"address": address, "rt": rt}


decoder_map = {
    "R": decode_r_type,
    "I": decode_i_type,
    "D": decode_d_type,
    "B": decode_b_type,
    "CB": decode_cb_type,
}


def get_register_name(reg_num):
    special_registers = {
        16: "IP0",
        17: "IP1",
        28: "SP",
        29: "FP",
        30: "LR",
        31: "XZR",
    }

    if reg_num in special_registers:
        return special_registers[reg_num]

    return f"X{reg_num}"


def format_r_type(name, fields, line_number=None):
    rm = get_register_name(fields["rm"])
    shamt = fields["shamt"]
    rn = get_register_name(fields["rn"])
    rd = get_register_name(fields["rd"])

    if name == "BR":
        return f"BR {rn}"

    if name == "LSL":
        return f"LSL {rd}, {rn}, #{shamt}"

    if name == "LSR":
        return f"LSR {rd}, {rn}, #{shamt}"

    if name == "DUMP":
        return "DUMP"

    if name == "HALT":
        return "HALT"

    if name == "PRNL":
        return "PRNL"

    if name == "PRNT":
        return f"PRNT {rd}"

    return f"{name} {rd}, {rn}, {rm}"


def format_i_type(name, fields, line_number=None):
    immediate = fields["immediate"]
    rn = get_register_name(fields["rn"])
    rd = get_register_name(fields["rd"])
    return f"{name} {rd}, {rn}, #{immediate}"


def format_d_type(name, fields, line_number=None):
    address = fields["address"]
    rn = get_register_name(fields["rn"])
    rt = get_register_name(fields["rt"])
    return f"{name} {rt}, [{rn}, #{address}]"


def format_b_type(name, fields, line_number):
    address = fields["address"]
    target_line = line_number + address
    return f"{name} label{target_line}"


def format_cb_type(name, fields, line_number):
    address = fields["address"]
    rt = fields["rt"]

    target_line = line_number + address

    if name == "B.cond":
        if rt in condition_codes:
            condition = condition_codes[rt]
            return f"B.{condition} label{target_line}"

    rt = get_register_name(fields["rt"])
    return f"{name} {rt}, label{target_line}"


format_map = {
    "R": format_r_type,
    "I": format_i_type,
    "D": format_d_type,
    "B": format_b_type,
    "CB": format_cb_type,
}


def main():
    # argument parser
    parser = argparse.ArgumentParser()
    # require input filename
    parser.add_argument("filename")
    args = parser.parse_args()

    line_number = 1

    # open file and read in the first 4 bytes
    with open(args.filename, "rb") as f:
        data = f.read(4)
        while data:
            b0, b1, b2, b3 = data
            # manually construct a 32-bit integer correlating to an instruction
            instruction = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

            opcode_6_bit = instruction >> 26 & 0x3F
            opcode_8_bit = instruction >> 24 & 0xFF
            opcode_10_bit = instruction >> 22 & 0x3FF
            opcode_11_bit = instruction >> 21 & 0x7FF
            for opcode in [opcode_6_bit, opcode_8_bit, opcode_10_bit, opcode_11_bit]:
                if opcode in opcodes:
                    name = opcodes[opcode]["instruction"]
                    type = opcodes[opcode]["type"]

                    if type in decoder_map:
                        fields = decoder_map[type](instruction)
                        formatted_instruction = format_map[type](name, fields, line_number)
                        print(f"label{line_number}:")
                        print(formatted_instruction)

            data = f.read(4)
            line_number += 1


if __name__ == "__main__":
    main()
