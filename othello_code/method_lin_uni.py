from itertools import product

from blank_method import BlankMethod, Info
from function import HashFunction


class LinearUniversal(BlankMethod):
    def __init__(self, key_size, array_size, hash_num):
        super().__init__(array_size)
        self.key_size = key_size
        self.hash_funs = [HashFunction(key_size, self.hash_size, array_size) for _ in range(hash_num)]
        self.max_offset = 0

    def search(self, key):
        info = Info(
            type='lin.search',
            records=self.records,
            key_inc=key in self.array,
        )
        hash_codes = [h(key) for h in self.hash_funs]
        for offset, code in product(range(self.max_offset + 1), hash_codes):
            if offset == 0:
                info.hash += 1
            code = (code + offset) % self.array_size
            info.memory += 1
            if self.array[code] == key:
                return info
        info.failed = True
        return info

    def insert(self, key):
        info = Info(
            type='lin.insert',
            records=self.records,
            key_inc=key in self.array
        )
        place = None
        hash_codes = [h(key) for h in self.hash_funs]
        for offset, code in product(range(self.max_offset + 1), hash_codes):
            if offset == 0:
                info.hash += 1
            code = (code + offset) % self.array_size
            info.memory += 1
            if self.array[code] == key:
                info.memory += 1
                return info
            if self.array[code] == 0 and place is None:
                place = code

        if place is not None:
            self.records += 1
            self.array[place] = key
            info.memory += 1
            return info

        for offset, code in product(range(self.max_offset + 1, self.array_size), hash_codes):
            code = (code + offset) % self.array_size
            info.memory += 1
            if self.array[code] == 0:
                self.records += 1
                self.array[code] = key
                info.memory += 1
                self.max_offset = offset if offset > self.max_offset else self.max_offset
                return info
        info.failed = True
        return info

    def delete(self, key):
        info = Info(
            type='lin.delete',
            records=self.records,
            key_inc=key in self.array
        )
        hash_codes = [h(key) for h in self.hash_funs]
        for offset, code in product(range(self.max_offset + 1), hash_codes):
            if offset == 0:
                info.hash += 1
            code = (code + offset) % self.array_size
            info.memory += 1
            if self.array[code] == key:
                self.records -= 1
                self.array[code] = 0
                info.memory += 1
                return info
        info.failed = True
        return info
