import unittest

from xsvm.vm import Processor
from xsvm.parser import parse_line


class InstructionsExecutionTestCase(unittest.TestCase):
    def setUp(self):
        self.proc = Processor()

    def test_mov_const_to_reg(self):
        instr = parse_line("mov r0, #1")
        self.proc.execute_instruction(instr)

        self.assertEqual(self.proc.register_bank.get("r0"), 1)

    def test_add_const_to_reg(self):
        instr_1 = parse_line("mov r1, #5")
        instr_2 = parse_line("add r0, r1, #2")

        self.proc.execute_instruction(instr_1)
        self.proc.execute_instruction(instr_2)

        self.assertEqual(self.proc.register_bank.get("r1"), 5)
        self.assertEqual(self.proc.register_bank.get("r0"), 7)

    def test_sub_const_from_reg(self):
        instr_1 = parse_line("mov r1, #5")
        instr_2 = parse_line("sub r0, r1, #2")

        self.proc.execute_instruction(instr_1)
        self.proc.execute_instruction(instr_2)

        self.assertEqual(self.proc.register_bank.get("r1"), 5)
        self.assertEqual(self.proc.register_bank.get("r0"), 3)

    def test_mul_reg_and_const(self):
        instr_1 = parse_line("mov r1, #5")
        instr_2 = parse_line("mul r0, r1, #2")

        self.proc.execute_instruction(instr_1)
        self.proc.execute_instruction(instr_2)

        self.assertEqual(self.proc.register_bank.get("r1"), 5)
        self.assertEqual(self.proc.register_bank.get("r0"), 10)

    def test_mul_reg_and_reg(self):
        instr_1 = parse_line("mov r1, #5")
        instr_2 = parse_line("mov r2, #4")
        instr_3 = parse_line("mul r0, r1, r2")

        self.proc.execute_instruction(instr_1)
        self.proc.execute_instruction(instr_2)
        self.proc.execute_instruction(instr_3)

        self.assertEqual(self.proc.register_bank.get("r1"), 5)
        self.assertEqual(self.proc.register_bank.get("r2"), 4)
        self.assertEqual(self.proc.register_bank.get("r0"), 20)

    def test_mla_reg_reg_const(self):
        instr_1 = parse_line("mov r1, #5")
        instr_2 = parse_line("mov r2, #4")
        instr_3 = parse_line("mla r0, r1, r2, #3")

        self.proc.execute_instruction(instr_1)
        self.proc.execute_instruction(instr_2)
        self.proc.execute_instruction(instr_3)

        self.assertEqual(self.proc.register_bank.get("r1"), 5)
        self.assertEqual(self.proc.register_bank.get("r2"), 4)
        self.assertEqual(self.proc.register_bank.get("r0"), 23)

if __name__ == '__main__':
    unittest.main()
