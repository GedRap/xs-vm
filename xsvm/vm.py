import instructions
from tabulate import tabulate

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

    def dump_content(self):
        table_content = []
        for i in range(0, 16, 2):
            reg_left = "r{r}".format(r=i)
            reg_right = "r{r}".format(r=i+1)
            table_content.append([reg_left, self.get(reg_left), reg_right, self.get(reg_right)])

        return tabulate(table_content, tablefmt="fancy_grid")

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
    def __init__(self, debug=False):
        self.register_bank = RegisterBank()
        self.memory = Memory()

        self.instructions_executed = 0
        self.halted = False
        self.comparison_register = 0

        self.register_bank.set("sp", 0xFFFFFF)

        self.instructions_executed_grouped = {}

        self.debug = debug

    def fetch_instruction(self):
        pc = self.register_bank.get("pc")
        instruction = self.memory.get(pc)

        if not isinstance(instruction, instructions.Instruction):
            raise RuntimeError("No instruction located at {addr}".format(addr=pc))

        if self.debug:
            print("Executing {i} from {a}".format(i=instruction.original_instruction, a=pc))

        self.register_bank.set("pc", pc + 1)

        return instruction

    def execute_instruction(self, instruction):
        if self.halted:
            return

        executable_name = "exec_" + instruction.mnemonic
        executable = getattr(instructions, executable_name)
        executable(self, instruction)
        self.instructions_executed += 1

        if instruction.mnemonic not in self.instructions_executed_grouped:
            self.instructions_executed_grouped[instruction.mnemonic] = 0

        self.instructions_executed_grouped[instruction.mnemonic] += 1

        if self.debug:
            print("Register bank after executing the instruction:")
            print(self.register_bank.dump_content())

    def halt(self):
        self.halted = True

    def step(self):
        self.execute_instruction(self.fetch_instruction())

    def execute_until_halted(self, instructions_limit=None):
        while not self.halted:
            if instructions_limit is not None and self.instructions_executed == instructions_limit:
                break
            self.step()

    def dump_instructions_executed_grouped(self):
        keys = self.instructions_executed_grouped.keys()
        table_contents = []
        for i in range(0, len(keys) + 1, 2):
            table_row = []
            if len(keys) > i:
                mnemonic_left = keys[i]
                count_left = self.instructions_executed_grouped[mnemonic_left]
                table_row.append(mnemonic_left)
                table_row.append(count_left)
            if len(keys) > i + 1:
                mnemonic_right = keys[i+1]
                count_right = self.instructions_executed_grouped[mnemonic_right]
                table_row.append(mnemonic_right)
                table_row.append(count_right)

            if len(table_row) > 0:
                table_contents.append(table_row)

        if len(table_contents) > 1:
            headers = ["Instruction", "Count", "Instruction", "Count"]
        else:
            headers = ["Instruction", "Count"]

        return tabulate(table_contents, headers=headers, tablefmt="fancy_grid")
