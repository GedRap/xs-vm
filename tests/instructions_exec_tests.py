import unittest

from xsvm.vm import Processor
from xsvm.parser import parse_line, load_into_memory
import xsvm.instructions


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

    def test_cmp(self):
        instr_1 = parse_line("mov r0, #5")
        instr_2 = parse_line("cmp r0, #3")

        self.proc.execute_instruction(instr_1)
        self.proc.execute_instruction(instr_2)

        self.assertGreater(self.proc.comparison_register, 0)

    def test_swi_0_functionally_correct(self):
        swi_instruction = parse_line("swi #0")
        processor = Processor()
        processor.execute_instruction(swi_instruction)

        self.assertEqual(processor.instructions_executed, 1)
        self.assertTrue(processor.halted)

    def test_swi_unhandled_interrupt(self):
        swi_instruction = parse_line("swi #99")
        processor = Processor()
        self.assertRaises(RuntimeError, lambda : processor.execute_instruction(swi_instruction))

    def test_beq_not_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #5", "cmp r0, #6", "beq foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step() # beq

        self.assertEqual(self.proc.register_bank.get("pc"), 3)

    def test_beq_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #5", "cmp r0, #5", "beq foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step() # beq

        self.assertEqual(self.proc.register_bank.get("pc"), 4)

    def test_bne_not_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #5", "cmp r0, #5", "bne foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step() # bne

        self.assertEqual(self.proc.register_bank.get("pc"), 3)

    def test_bne_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #5", "cmp r0, #6", "bne foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step() # bne

        self.assertEqual(self.proc.register_bank.get("pc"), 4)

    def test_blt_not_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #7", "cmp r0, #5", "blt foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step()

        self.assertEqual(self.proc.register_bank.get("pc"), 3)

    def test_blt_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #5", "cmp r0, #6", "blt foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step()

        self.assertEqual(self.proc.register_bank.get("pc"), 4)

    def test_bgt_not_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #4", "cmp r0, #5", "bgt foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step()

        self.assertEqual(self.proc.register_bank.get("pc"), 3)

    def test_bgt_performed(self):
        load_into_memory(self.proc.memory, ["mov r0, #8", "cmp r0, #6", "bgt foobar", "nop", "foobar nop"])

        self.proc.step()
        self.proc.step()
        self.proc.step()

        self.assertEqual(self.proc.register_bank.get("pc"), 4)

    def test_push(self):
        load_into_memory(self.proc.memory, ["mov r0, #5", "push r0"])

        self.proc.step()
        self.proc.step()

        sp = self.proc.register_bank.get("sp")

        self.assertEqual(self.proc.memory.get(sp), 5)

    def test_pop(self):
        load_into_memory(self.proc.memory, ["mov r0, #5", "mov r1, #9", "push r0", "push r1", "pop r2", "pop r3"])

        self.proc.step()
        self.proc.step()
        self.proc.step()
        self.proc.step()
        self.proc.step()
        self.proc.step()

        self.assertEqual(self.proc.register_bank.get("r2"), 9)
        self.assertEqual(self.proc.register_bank.get("r3"), 5)

if __name__ == '__main__':
    unittest.main()
