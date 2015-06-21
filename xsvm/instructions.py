class Instruction:
    def __init__(self, mnemonic, operands, label):
        self.mnemonic = mnemonic
        self.operands = operands
        self.label = label

supported_instructions = ["mov", "add", "nop", "b"]