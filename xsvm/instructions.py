import sys

class Instruction:
    def __init__(self, mnemonic, operands, label):
        self.mnemonic = mnemonic
        self.operands = operands
        self.label = label

supported_instructions = ["mov", "add", "sub", "mul", "mla", "nop", "b", "str", "swi", "cmp", "beq", "bne", "blt", "bgt"]


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
                raise RuntimeError("Can't extract register value if the processor is not passed")

            return processor.register_bank.get(self.value)

        if self.type == Operand.TYPE_LABEL:
            if processor is None:
                raise RuntimeError("Can't resolve a label if the processor is not passed")

            label = self.value
            resolved_label = processor.memory.resolve_label(label)

            return resolved_label


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


def exec_cmp(proc, instr):
    op1 = instr.operands[0].extract_value(proc)
    op2 = instr.operands[1].extract_value(proc)

    proc.comparison_register = op1 - op2


def exec_beq(proc, instr):
    if proc.comparison_register == 0:
        new_pc = instr.operands[0].extract_value(proc)
        proc.register_bank.set("pc", new_pc)


def exec_bne(proc, instr):
    if proc.comparison_register != 0:
        new_pc = instr.operands[0].extract_value(proc)
        proc.register_bank.set("pc", new_pc)


def exec_blt(proc, instr):
    if proc.comparison_register < 0:
        new_pc = instr.operands[0].extract_value(proc)
        proc.register_bank.set("pc", new_pc)


def exec_bgt(proc, instr):
    if proc.comparison_register > 0:
        new_pc = instr.operands[0].extract_value(proc)
        proc.register_bank.set("pc", new_pc)


def exec_swi(proc, instr):
    interrupt_number = instr.operands[0].extract_value(proc)
    executable_name = "exec_swi_" + str(interrupt_number)

    try:
        current_module = sys.modules[__name__]
        executable = getattr(current_module, executable_name)
    except AttributeError:
        raise RuntimeError("Unhandled software interrupt {swi}".format(swi=interrupt_number))

    executable(proc, instr)


def exec_swi_0(proc, instr):
    proc.halt()