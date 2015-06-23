import instructions

class Memory:
    def __init__(self):
        self.memory_storage = {}
        self.labels_map = {}

    def set(self, address, value):
        self.memory_storage[address] = value

    def set_label(self, label, address):
        self.labels_map[label] = address

    def get(self, address):
        return self.memory_storage.get(address, 0)

    def resolve_label(self, label):
        if label not in self.labels_map:
            raise RuntimeError("Could not resolve label {l}".format(l=label))

        return self.labels_map[label]


class RegisterBank:
    available_registers = [
        "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"
    ]
    aliases = {"sp": "r13", "lr": "r14", "pc": "r15"}

    def __init__(self):
        self.registers = {}
        for register in RegisterBank.available_registers:
            self.registers[register] = 0

    def get(self, register):
        register = RegisterBank._resolve_alias(register)
        RegisterBank._validate_register_name(register)

        return self.registers[register]

    def set(self, register, value):
        register =RegisterBank._resolve_alias(register)
        RegisterBank._validate_register_name(register)

        self.registers[register] = value

    @staticmethod
    def _resolve_alias(register):
        if register in RegisterBank.aliases:
            register = RegisterBank.aliases[register]

        return register

    @staticmethod
    def _validate_register_name(register):
        if register not in RegisterBank.available_registers:
            raise AttributeError("{r} is an invalid register".format(r=register))


class Processor:
    def __init__(self):
        self.register_bank = RegisterBank()
        self.memory = Memory()
        self.instructions_executed = 0
        self.halted = False
        self.comparison_register = 0

    def fetch_instruction(self):
        pc = self.register_bank.get("pc")
        instruction = self.memory.get(pc)

        if not isinstance(instruction, instructions.Instruction):
            raise RuntimeError("No instruction located at {addr}".format(addr=pc))

        self.register_bank.set("pc", pc + 1)

        return instruction

    def execute_instruction(self, instruction):
        if self.halted:
            return

        executable_name = "exec_" + instruction.mnemonic
        executable = getattr(instructions, executable_name)
        executable(self, instruction)
        self.instructions_executed += 1

    def halt(self):
        self.halted = True
