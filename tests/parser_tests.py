import unittest

from xsvm.parser import parse_line, load_into_memory
from xsvm.instructions import Operand
from xsvm.vm import Memory

class ParserTestCase(unittest.TestCase):
    def test_instruction_no_operands_no_label(self):
        parsed = parse_line("nop")

        self.assertEqual(parsed.mnemonic, "nop")
        self.assertIsNone(parsed.label)
        self.assertIsNone(parsed.operands)

    def test_instruction_single_operand(self):
        parsed = parse_line("b halt")

        self.assertEqual(parsed.mnemonic, "b")
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_LABEL)
        self.assertEqual(parsed.operands[0].value, "halt")
        self.assertIsNone(parsed.label)

    def test_mov_without_label_constant_to_register(self):
        parsed = parse_line("mov r1, #5")

        self.assertEqual(parsed.label, None)
        self.assertEqual(parsed.mnemonic, "mov")
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "r1")
        self.assertEqual(parsed.operands[1].type, Operand.TYPE_CONSTANT)
        self.assertEqual(parsed.operands[1].value, 5)
        self.assertEqual(len(parsed.operands), 2)

    def test_mov_with_label_constant_to_register(self):
        parsed = parse_line("hello mov r1, #5")

        self.assertEqual(parsed.label, "hello")
        self.assertEqual(parsed.mnemonic, "mov")
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "r1")
        self.assertEqual(parsed.operands[1].type, Operand.TYPE_CONSTANT)
        self.assertEqual(parsed.operands[1].value, 5)
        self.assertEqual(len(parsed.operands), 2)

    def test_store_register_to_memory(self):
        parsed = parse_line("str r0, [r1]")

        self.assertIsNone(parsed.label)
        self.assertEqual(parsed.mnemonic, "str")
        self.assertEqual(len(parsed.operands), 2)
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "r0")
        self.assertEqual(parsed.operands[1].type, Operand.TYPE_INDIRECT_ADDRESS)
        self.assertEqual(parsed.operands[1].value, "r1")

    def test_label_with_colon(self):
        parsed = parse_line("foobar: str r0, [r1]")

        self.assertEqual(parsed.label, "foobar:")
        self.assertEqual(parsed.mnemonic, "str")
        self.assertEqual(len(parsed.operands), 2)
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "r0")
        self.assertEqual(parsed.operands[1].type, Operand.TYPE_INDIRECT_ADDRESS)
        self.assertEqual(parsed.operands[1].value, "r1")

    def test_parse_register_alias(self):
        parsed = parse_line("push lr")

        self.assertIsNone(parsed.label)
        self.assertEqual(parsed.mnemonic, "push")
        self.assertEqual(len(parsed.operands), 1)
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_REGISTER)
        self.assertEqual(parsed.operands[0].value, "lr")

    def test_parse_label_which_partially_matches_instruction(self):
        parsed = parse_line("bl addition")

        self.assertIsNone(parsed.label)
        self.assertEqual(parsed.mnemonic, "bl")
        self.assertEqual(len(parsed.operands), 1)
        self.assertEqual(parsed.operands[0].type, Operand.TYPE_LABEL)
        self.assertEqual(parsed.operands[0].value, "addition")

    def test_load_into_memory(self):
        source_code = ["mov r0, #1", "mov r1, #5"]
        test_memory = Memory()

        load_into_memory(test_memory, source_code)

        self.assertEqual(test_memory.get(2), 0)

        inst_1 = test_memory.get(0)
        inst_2 = test_memory.get(1)

        self.assertEqual(inst_1.mnemonic, "mov")
        self.assertEqual(inst_1.operands[0].value, "r0")
        self.assertEqual(inst_1.operands[1].value, 1)

        self.assertEqual(inst_2.mnemonic, "mov")
        self.assertEqual(inst_2.operands[0].value, "r1")
        self.assertEqual(inst_2.operands[1].value, 5)

if __name__ == '__main__':
    unittest.main()
