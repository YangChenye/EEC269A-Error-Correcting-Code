# Copyright (c) 2023 Chenye Yang

import channel
from Utils import polyTools

import numpy as np


tx_msg = np.array([0, 1, 0, 0, 1, 0, 0, 0, 0, 1], dtype=np.uint8) # 10 bits
print("Original bits:", tx_msg)

# Channel
chl = channel.Channel()

# Work with (15, 11) cyclic code
n = 15
k = 11

# Create the generator matrix
genMatrix_decimal = polyTools.findMatrix(n, k)
G = polyTools.genMatrixDecmial2Ndarray(genMatrix_decimal, n)


cyclic_code = channel.Cyclic_Code(G)

# Encoding
tx_codewords = cyclic_code.encoder_systematic(tx_msg)
print("Encoded bits      :", tx_codewords)

# Passing through the channel
rx_codewords = chl.binary_symmetric_channel(tx_codewords, 0.1)
print("Bits after channel:", rx_codewords)

# Correction with syndrome look-up table
estimated_tx_codewords = cyclic_code.corrector_syndrome(rx_codewords)
print("Estimated TX bits :", estimated_tx_codewords)

# Decoding
padding_length = k - (len(tx_msg) % k)
rx_msg = cyclic_code.decoder_systematic(estimated_tx_codewords, padding_length)
print("Decoded bits :", rx_msg)