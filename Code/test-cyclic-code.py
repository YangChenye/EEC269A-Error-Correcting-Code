# Copyright (c) 2023 Chenye Yang

import channel
from Utils import stat_analysis

import numpy as np


tx_msg = np.array([0, 1, 0, 0, 1, 0, 0, 0, 0, 1], dtype=np.uint8) # 10 bits
print("Original bits:", tx_msg)

# Channel
chl = channel.Channel()

# Work with (15, 11) cyclic code
n = 15
k = 5

# Create the generator matrix
# genMatrix_decimal = polyTools.findMatrix(n, k)
# G = polyTools.genMatrixDecmial2Ndarray(genMatrix_decimal, n)


cyclic_code = channel.Cyclic_Code(n,k,None)

# Encoding
tx_codewords = cyclic_code.encoder_systematic(tx_msg)
print("Encoded bits      :", tx_codewords)

# Passing through the channel
rx_codewords = chl.binary_symmetric_channel(tx_codewords, 0.1)
print("Bits after channel:", rx_codewords)


# Statistic analysis
correct_codewords = stat_analysis.num_codeword_with_t_errors(tx_codewords, rx_codewords, 0, n)
one_error_codewords = stat_analysis.num_codeword_with_t_errors(tx_codewords, rx_codewords, 1, n)
total_codewords = len(tx_codewords) // n
uncorrectable_codewords = total_codewords - correct_codewords - one_error_codewords
print("Channel statistic analysis:")
print("Total codewords:", total_codewords)
print("Correct codewords:", correct_codewords)
print("One error codewords:", one_error_codewords)
print("Uncorrectable codewords:", uncorrectable_codewords)


# Without correction
# Decoding
padding_length = (k - len(tx_msg)) % k
rx_msg = cyclic_code.decoder_systematic(rx_codewords, padding_length)
print("Before correction:")
print("Decoded bits without correction:", rx_msg)
print("Number of correct bits:", stat_analysis.num_correct_bits(tx_msg, rx_msg))


# Correction with syndrome look-up table
estimated_tx_codewords = cyclic_code.corrector_trapping(rx_codewords)
print("After correction:")
print("Estimated TX bits :", estimated_tx_codewords)
# Decoding
padding_length = (k - len(tx_msg)) % k
rx_msg = cyclic_code.decoder_systematic(estimated_tx_codewords, padding_length)
print("Decoded bits :", rx_msg)
print("Number of correct bits:", stat_analysis.num_correct_bits(tx_msg, rx_msg))