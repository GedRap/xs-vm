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

    def test_set_label(self):
        self.memory.set_label("foo", 1)
        self.assertEqual(self.memory.labels_map["foo"], 1)

    def test_resolve_label_existing(self):
        self.memory.labels_map["foobar"] = 4
        self.assertEqual(self.memory.resolve_label("foobar"), 4)

    def test_resolve_label_not_existing(self):
        self.assertRaises(RuntimeError, lambda : self.memory.resolve_label("blah"))

if __name__ == '__main__':
    unittest.main()
