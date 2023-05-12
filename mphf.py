from pybbhash.bbhash import PyMPHF

def build_mphf(K : set):
    return PyMPHF(list(K), len(K), 1, 1.0)

def mphf_no_false_negatives_sanity_check(mphf, K : set):
    for key in K:
        idx = mphf.lookup(key)
        assert idx is not None and idx < len(K)

def mphf_query(mphf, K : set, K_prime : set):
    count = 0
    for key in K_prime:
        idx = mphf.lookup(key)
        if idx is not None and idx < len(K):
            count += 1
    return count
