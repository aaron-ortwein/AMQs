import random
import uuid
from bloom_filter2 import BloomFilter

def rand_kmer(k : int = 31):
    return ''.join(random.choices(["A", "C", "G", "T"], k=k))

def rand_uint64():
    return uuid.uuid4().int & ((1 << 64) - 1)

def generate_K(size : int, rand_key):
    random.seed(0)
    K = set()
    while len(K) < size:
        K.add(rand_key())
    return K

def generate_K_prime(K : set, positive_keys_density : float, rand_key) -> BloomFilter:
    assert 0 <= positive_keys_density <= 1
    size = len(K)

    num_positive_keys = round(size * positive_keys_density)
    positive_keys = set(random.sample(sorted(K), num_positive_keys))

    negative_keys = set()
    while len(negative_keys) < size - num_positive_keys:
        key = rand_key()
        if key not in positive_keys:
            negative_keys.add(key)
    
    return positive_keys | negative_keys
