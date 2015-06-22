import unittest
from mock import patch

from xsvm.parser import parse_line, load_into_memory
from xsvm.vm import Processor
import xsvm.instructions

class ProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.cpu = Processor()

    def test_fetch_valid_instruction(self):
        load_into_memory(self.cpu.memory, ["mov r0, #1", "mov r1, #5"])

        inst_1 = self.cpu.fetch_instruction()

        self.assertEqual(self.cpu.register_bank.get("pc"), 1)
        self.assertEqual(self.cpu.instructions_executed, 0)

        self.assertEqual(inst_1.mnemonic, "mov")
        self.assertEqual(inst_1.operands[0].value, "r0")
        self.assertEqual(inst_1.operands[1].value, 1)

        inst_2 = self.cpu.fetch_instruction()

        self.assertEqual(self.cpu.register_bank.get("pc"), 2)
        self.assertEqual(inst_2.mnemonic, "mov")
        self.assertEqual(inst_2.operands[0].value, "r1")
        self.assertEqual(inst_2.operands[1].value, 5)

    def test_fetch_non_instruction(self):
        self.assertRaises(RuntimeError, lambda: self.cpu.fetch_instruction())

    @patch.object(xsvm.instructions, 'exec_nop')
    def test_execute_instruction(self, mock):
        nop_instruction = parse_line("nop")
        processor = Processor()
        processor.execute_instruction(nop_instruction)

        self.assertTrue(mock.called)
        self.assertEqual(processor.instructions_executed, 1)

    @patch.object(xsvm.instructions, 'exec_nop')
    def test_halting(self, mock):
        nop_instruction = parse_line("nop")
        processor = Processor()
        processor.halt()
        processor.execute_instruction(nop_instruction)

        self.assertFalse(mock.called)
        self.assertEqual(processor.instructions_executed, 0)

if __name__ == '__main__':
    unittest.main()
