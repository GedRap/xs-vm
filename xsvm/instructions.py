class Instruction:
    def __init__(self, mnemonic, operands, label):
        self.mnemonic = mnemonic
        self.operands = operands
        self.label = label

supported_instructions = ["mov", "add", "nop", "b", "str"]

class Operand:
    TYPE_REGISTER = "register"
    TYPE_INDIRECT_ADDRESS = "indirect_address"
    TYPE_CONSTANT = "constant"
    TYPE_LABEL = "label"

    def __init__(self, type, value):
        self.type = type
        self.value = value
