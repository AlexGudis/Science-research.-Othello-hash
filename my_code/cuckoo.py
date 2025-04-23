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
    



    # return string representation of both tables
    def __str__(self):
        str1 = "Table 1: [ " + str(self.array1[0]) 
        str2 = " Table 2: [ " + str(self.array2[0]) 
        for i in range(1, self.size):
            str1 += ", " + str(self.array1[i])
        str1 += "]"

        for i in range(1, self.size):
           str2 += ", " + str(self.array2[i]) 
        str2 += "]"
        
        return str1 + str2 
    


    # get new hash functions and reinsert everything 
    def rehash(self, size):
        self.hash1, self.hash2 = random.sample(hash_functions, 2)          # get new hash functions
        
        temp = HashTab(size)    # create new hash tables

        # re-hash each item and insert it into the correct position in the new tables
        for i in range(self.size // 2):
            x = self.array1[i]
            y = self.array2[i]
            if x != None:
                temp.insert(x.key, x.data)
            if y != None:
                temp.insert(y.key, y.data)

        # save new tables 
        self.array1 = temp.array1
        self.array2 = temp.array2
        self.keys_cnt = temp.keys_cnt
        self.size = temp.size


    # Increase the hash table's size x 2 
    def growHash(self):
        newSize = self.size * 2
        # re-hash each item and insert it into the
        # correct position in the new table
        self.rehash(newSize)
    

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