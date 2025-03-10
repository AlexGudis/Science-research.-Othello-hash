from recordclass import RecordClass
from math import log2, ceil


class Info(RecordClass):
    type:     str = ''
    records:  int = 0
    key_inc: bool = False
    memory:   int = 0
    hash:     int = 0
    failed:   bool = False


class BlankMethod:
    def __init__(self, array_size: int):
        self.array_size = array_size
        self.hash_size = ceil(log2(array_size))
        self.array = [0] * array_size
        self.records = 0
        self.fatal = False

    def search(self, key: int) -> Info:
        pass

    def insert(self, key: int) -> Info:
        pass

    def delete(self, key: int) -> Info:
        pass
