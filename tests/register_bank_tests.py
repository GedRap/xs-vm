import unittest

from xsvm.vm import RegisterBank

class RegisterBankTestCase(unittest.TestCase):
    def setUp(self):
        self.rb = RegisterBank()

    def test_get(self):
        self.assertEqual(self.rb.registers["r0"], self.rb.get("r0"))

    def test_get_alias(self):
        self.assertEqual(self.rb.registers["r15"], self.rb.get("pc"))

    def test_get_invalid(self):
        self.assertRaises(AttributeError, lambda: self.rb.get("x"))

    def test_set(self):
        self.rb.set("r0", 11)
        self.assertEqual(self.rb.registers["r0"], 11)

    def test_set_alias(self):
        self.rb.set("pc", 10)
        self.assertEqual(self.rb.registers["r15"], 10)

    def test_set_invalid(self):
        self.assertRaises(AttributeError, lambda: self.rb.set("x", 1))

if __name__ == '__main__':
    unittest.main()
