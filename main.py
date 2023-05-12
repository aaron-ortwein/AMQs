import time
import os
import sys

from bloom_filter import build_bloom_filter, bloom_filter_no_false_negatives_sanity_check, bloom_filter_query
from mphf import build_mphf, mphf_no_false_negatives_sanity_check, mphf_query
from fingerprint_array import mphf_fp, mphf_fp_no_false_negatives_sanity_check, mphf_fp_query
from setutils import rand_uint64, generate_K, generate_K_prime

K_sizes = [1000, 10000, 100000]
positive_key_densities = [0.25, 0.5, 0.75]
exponents = [7, 8, 10]

for size in K_sizes:
    K = generate_K(size, rand_uint64)

    for positive_key_density in positive_key_densities:
        K_prime = generate_K_prime(K, positive_key_density, rand_uint64)
        assert len(K) == len(K_prime)

        print(f"=== Testing Parameters: |K| = {size}, fraction positive keys = {positive_key_density} ===")
        print()

        for exponent in exponents:
            error_rate = 1 / (2 ** exponent)

            # Testing Bloom Filter
            bloom_filter = build_bloom_filter(error_rate, K)
            bloom_filter_no_false_negatives_sanity_check(bloom_filter, K)
            
            start = time.time()
            positives = bloom_filter_query(bloom_filter, K_prime)
            end = time.time()

            fp_rate = (positives - round(positive_key_density * len(K))) / len(K_prime - K)
            
            print(f"Bloom Filter Size (Bits): {bloom_filter.num_bits_m}")
            print(f"Expected FP Rate: {error_rate}")
            print(f"Actual FP Rate: {fp_rate}")
            print(f"Query Time (s): {end - start}")
            print()

            # Testing MPHF with fingerprint array
            mphf, fp = mphf_fp(K, exponent)
            mphf_fp_no_false_negatives_sanity_check(mphf, fp, exponent, K)

            start = time.time()
            positives = mphf_fp_query(mphf, fp, exponent, K_prime)
            end = time.time()

            fp_rate = (positives - round(positive_key_density * len(K))) / len(K_prime - K)

            mphf_bits = mphf.get_mem()
            print(f"Theoretical MPHF + FP Size (Bits): {mphf_bits + len(fp) * exponent}")
            print(f"Actual MPHF + FP Size (Bits): {mphf_bits + 8 * fp.__sizeof__()}")
            print(f"Expected FP Rate: {error_rate}")
            print(f"Actual FP Rate: {fp_rate}")
            print(f"Query Time (s): {end - start}")
            print()

        # Testing MPHF
        mphf = build_mphf(K)
        mphf_no_false_negatives_sanity_check(mphf, K)

        start = time.time()
        positives = mphf_query(mphf, K, K_prime)
        end = time.time()

        fp_rate = (positives - round(positive_key_density * len(K))) / len(K_prime - K)

        mphf_bits = mphf.get_mem()
        print(f"MPHF Size (Bits): {mphf_bits}")
        print(f"Actual FP Rate: {fp_rate}")
        print(f"Query Time (s): {end - start}")
        print()

        print("=======================================================================")
