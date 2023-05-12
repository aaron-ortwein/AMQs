from pybbhash.bbhash import PyMPHF

def mphf_fp(K : set, bits : int):
    mphf = PyMPHF(list(K), len(K), 1, 1.0)
    fp = [0] * len(K)
    mask = (1 << bits) - 1
    for key in K:
        fp[mphf.lookup(key)] = hash(key) & mask
    return mphf, fp

def mphf_fp_no_false_negatives_sanity_check(mphf, fp, bits : int, K : set):
    mask = (1 << bits) - 1
    for key in K:
        idx = mphf.lookup(key)
        assert idx is not None and hash(key) & mask == fp[idx]

def mphf_fp_query(mphf, fp, bits : int, K_prime : set):
    count = 0
    mask = (1 << bits) - 1
    for key in K_prime:
        idx = mphf.lookup(key)
        if idx is not None and hash(key) & mask == fp[idx]:
            count += 1
    return count
