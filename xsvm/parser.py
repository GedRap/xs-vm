from pyparsing import *
from instructions import supported_instructions, Instruction, Operand

label_definition = Word(alphanums + "_" + ":")
mnemonic_definition = oneOf(" ".join(supported_instructions), caseless=True) + FollowedBy(White() | LineEnd())
register_definition = Combine(CaselessLiteral("r") + Word(nums)) | oneOf("lr pc sp")
indirectly_addressed_register = Combine(Literal("[") + register_definition + Literal("]"))
constant_definition = Combine(Literal("#") + Word(nums))

operand_definitions = register_definition | indirectly_addressed_register | label_definition | constant_definition


def parse_line(source_code_line):
    if source_code_line == "":
        return None

    instruction_definition = Forward()

    instruction_definition << Optional(label_definition.setResultsName("label") + FollowedBy(mnemonic_definition)) + mnemonic_definition.setResultsName("mnemonic") \
                              + Optional(Group(delimitedList(operand_definitions, ","))).setResultsName("operands")

    parsed_line = instruction_definition.parseString(source_code_line)

    label = parsed_line.label
    if label == "":
        label = None

    mnemonic = parsed_line.mnemonic
    if mnemonic == "" and len(mnemonic) is 0:
        mnemonic = None
    else:
        mnemonic = mnemonic[0]

    if parsed_line.operands == "":
        operands = None
    else:
        operands_raw = parsed_line.operands[0]
        operands = process_operands(operands_raw)

    parsed_instruction = Instruction(label=label, mnemonic=mnemonic, operands=operands)

    return parsed_instruction


def process_operands(operands_raw):
    operands = []
    for operand_raw in operands_raw:
        try:
            register_definition.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_REGISTER, value=operand_raw)
            operands.append(new_operand)
            continue
        except:
            pass

        try:
            indirectly_addressed_register.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_INDIRECT_ADDRESS, value=operand_raw.replace("[", "", 1).replace("]", "", 1))
            operands.append(new_operand)
            continue
        except:
            pass

        try:
            label_definition.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_LABEL, value=operand_raw)
            operands.append(new_operand)
            continue
        except:
            pass

        try:
            constant_definition.parseString(operand_raw)
            new_operand = Operand(type=Operand.TYPE_CONSTANT, value=int(operand_raw.replace("#", "", 1)))
            operands.append(new_operand)
            continue
        except:
            pass

    return operands


def load_into_memory(memory, source_code):
    memory_pointer = 0
    for source_code_line in source_code:
        parsed_line = parse_line(source_code_line)
        if parsed_line is not None:
            memory.set(memory_pointer, parsed_line)

            if parsed_line.label is not None:
                memory.set_label(parsed_line.label, memory_pointer)

            memory_pointer += 1


def load_file_into_memory(memory, filename):
    file_handler = open(filename)
    lines_read = [line_read.strip() for line_read in file_handler]

    load_into_memory(memory, lines_read)