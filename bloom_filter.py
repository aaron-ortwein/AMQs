from bloom_filter2 import BloomFilter

def build_bloom_filter(error_rate : float, K : set):
    bloom_filter = BloomFilter(max_elements=len(K), error_rate=error_rate)
    for key in K:
        bloom_filter.add(key)
    return bloom_filter

# Pre-Condition: K is the set originally inserted into the bloom filter
def bloom_filter_no_false_negatives_sanity_check(bloom_filter : BloomFilter, K : set):
    for key in K: assert key in bloom_filter

def bloom_filter_query(bloom_filter : BloomFilter, K_prime : set):
    count = 0
    for key in K_prime:
        if key in bloom_filter:
            count += 1
    return count
