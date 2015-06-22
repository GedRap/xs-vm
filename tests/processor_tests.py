import unittest

from xsvm.parser import load_into_memory
from xsvm.vm import Processor


class ProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.cpu = Processor()

    def test_fetch_valid_instruction(self):
        load_into_memory(self.cpu.memory, ["mov r0, #1", "mov r1, #5"])

        inst_1 = self.cpu.fetch_instruction()

        self.assertEqual(self.cpu.register_bank.get("pc"), 1)
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

if __name__ == '__main__':
    unittest.main()
