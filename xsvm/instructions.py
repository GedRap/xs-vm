class Instruction:
    def __init__(self, mnemonic, operands, label):
        self.mnemonic = mnemonic
        self.operands = operands
        self.label = label

supported_instructions = ["mov", "add", "sub", "mul", "mla", "nop", "b", "str"]


class Operand:
    TYPE_REGISTER = "register"
    TYPE_INDIRECT_ADDRESS = "indirect_address"
    TYPE_CONSTANT = "constant"
    TYPE_LABEL = "label"

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def extract_value(self, processor=None):
        if self.type == Operand.TYPE_CONSTANT:
            return self.value

        if self.type == Operand.TYPE_REGISTER:
            if processor is None:
                raise RuntimeError("Can't extract register value when processor is not set")

            return processor.register_bank.get(self.value)


def exec_nop(proc, instr):
    return


def exec_mov(proc, instr):
    to_move = instr.operands[1].extract_value(proc)

    proc.register_bank.set(instr.operands[0].value, to_move)


def exec_add(proc, instr):
    number_1 = instr.operands[1].extract_value(proc)
    number_2 = instr.operands[2].extract_value(proc)

    proc.register_bank.set(instr.operands[0].value, number_1 + number_2)


def exec_sub(proc, instr):
    number_1 = instr.operands[1].extract_value(proc)
    number_2 = instr.operands[2].extract_value(proc)

    proc.register_bank.set(instr.operands[0].value, number_1 - number_2)


def exec_mul(proc, instr):
    number_1 = instr.operands[1].extract_value(proc)
    number_2 = instr.operands[2].extract_value(proc)

    proc.register_bank.set(instr.operands[0].value, number_1 * number_2)


def exec_mla(proc, instr):
    number_1 = instr.operands[1].extract_value(proc)
    number_2 = instr.operands[2].extract_value(proc)
    number_3 = instr.operands[3].extract_value(proc)

    proc.register_bank.set(instr.operands[0].value, number_1 * number_2 + number_3)