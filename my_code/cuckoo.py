import hashlib
import random

hash_functions = [hashlib.sha1, hashlib.sha224, hashlib.sha256,
                  hashlib.sha384, hashlib.sha3_512, hashlib.sha512]

class HashTab():
    def __init__(self, size):
        self.array1 = [None] * (size // 2)  # create 2 arrays, both half the length of size
        self.array2 = [None] * (size // 2)
        self.hash1, self.hash2 = random.sample(hash_functions, 2) # random hash func for each array of the cuckoo
        self.keys_cnt = 0                 # total number of nodes 
        self.size = size                  # total size of hash table (both lists in summary)

    # return current number of keys in table    
    def __len__(self): return self.keys_cnt

    def hashFunc(self, s):
        x = self.hash1(s)         # hash twice 
        y = self.hash2(s)
        
        return x % self.size // 2, y % self.size // 2
    

    # Return data if there, otherwise return None
    def find(self, k):
        pos1, pos2 = self.hashFunc(k)               # check both positions the key/data
        x = self.array1[pos1]                       # could be in. return data if found.
        y = self.array2[pos2]                 
        if x != None and x.key == k:  return x.data
        if y != None and y.key == k:  return y.data
    
        # return None if the key can't be found     
        return None
    

    # delete the node associated with that key and return True on success
    def delete(self, k):
        pos1, pos2 = self.hashFunc(k)  
        x = self.array1[pos1]
        y = self.array2[pos2]
        if  x != None and  x.key == k:  self.array1[pos1] = None
        elif y != None and y.key == k:  self.array2[pos2] = None
        else:   return False   # the key wasnt found in either possible position
        self.keys_cnt -= 1 
        return True