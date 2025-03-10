import numpy as np


class HashFunction:
    def __init__(self, key_dim, hash_dim, max_val=None, *, salt=None, mat=None):
        self.dims = key_dim, hash_dim
        if mat is None:
            mat = np.random.randint(2, size=self.dims, dtype=bool)
        if salt is None:
            salt = np.random.randint(2, size=self.dims[0], dtype=bool)
        if max_val == 1 << hash_dim:
            max_val = None
        self.max_val = max_val
        self.pows = 1 << np.arange(key_dim), 1 << np.arange(hash_dim)
        self.mat = np.array(mat)
        self.salt = np.array(salt)

    def __call__(self, key: int):
        res = (key & self.pows[0]) > 0
        res = (res ^ self.salt).astype(int)
        res = np.dot(res, self.mat) % 2
        res = int((res * self.pows[1]).sum())
        if self.max_val is not None:
            res = (res * self.max_val) >> self.dims[1]
        return res
