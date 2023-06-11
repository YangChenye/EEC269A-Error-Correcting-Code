# Copyright (c) 2023 Chenye Yang

import numpy as np



def num_codeword_with_t_errors(original_bits, corrupted_bits, t, n):
    """
    Calculate how many codewords in the bit stream contains t error bits.

        @type  original_bits: ndarray
        @param original_bits: original bit stream

        @type  corrupted_bits: ndarray
        @param corrupted_bits: corrupted bit stream

        @type  t: int
        @param t: number of errors

        @type  n: int
        @param n: length of the codeword

        @rtype:   int
        @return:  number of codewords that contains exactly t errors
    """
    # Reshape the array so each row is a codeword
    original_bits = original_bits.reshape(-1, n)
    corrupted_bits = corrupted_bits.reshape(-1, n)

    # Modulo 2 addition
    diff = (original_bits + corrupted_bits) % 2

    # Count the number of 1s in each row
    result = np.count_nonzero(diff, axis=1)

    # Count the number of rows that contains exactly t 1s
    return np.count_nonzero(result == t)


def num_correct_messages(original_bits, corrupted_bits, k):
    """
    Calculate how many messages in the bit stream are correct.

        @type  original_bits: ndarray
        @param original_bits: original bit stream

        @type  corrupted_bits: ndarray
        @param corrupted_bits: corrupted bit stream

        @type  k: int
        @param k: length of the message

        @rtype:   int
        @return:  number of messages that are correct
    """
    # Reshape the array so each row is a message
    original_bits = original_bits.reshape(-1, k)
    corrupted_bits = corrupted_bits.reshape(-1, k)

    # Count the number of rows that are exactly the same
    return np.count_nonzero(np.all(original_bits == corrupted_bits, axis=1))


def num_correct_bits(original_bits, corrupted_bits):
    """
    Calculate how many bits in the bit stream are correct.

        @type  original_bits: ndarray
        @param original_bits: original bit stream

        @type  corrupted_bits: ndarray
        @param corrupted_bits: corrupted bit stream

        @rtype:   int
        @return:  number of bits that are correct
    """
    # Count the number of bits that are exactly the same
    return np.count_nonzero(original_bits == corrupted_bits)

