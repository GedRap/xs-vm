import unittest

from xsvm.vm import Memory

class MemoryTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_setting(self):
        self.memory.set(1, 2)
        self.assertEqual(self.memory.memory_storage[1], 2)

    def test_getting_set(self):
        self.memory.set(1, 3)
        self.assertEqual(self.memory.get(1), 3)

    def test_getting_not_set(self):
        self.assertEqual(self.memory.get(3333), 0)

if __name__ == '__main__':
    unittest.main()
