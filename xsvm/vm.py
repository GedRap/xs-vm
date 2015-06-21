class Memory:
    def __init__(self):
        self.memory_storage = {}

    def set(self, address, value):
        self.memory_storage[address] = value

    def get(self, address):
        return self.memory_storage.get(address, 0)