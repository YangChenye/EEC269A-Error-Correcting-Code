# Copyright (c) 2023 Chenye Yang

import numpy as np
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)



def create_parity_check_matrix(G):
    """
    Create the parity-check matrix, H = [I_{n-k} | P.T]

        @type  G: ndarray
        @param G: generator matrix in systematic form, G = [P | I_k]

        @rtype:   ndarray
        @return:  parity-check matrix
    """
    # Get the size of the generator matrix
    k, n = G.shape

    # Create the parity-check matrix
    # G = [P | I_k], Extract P
    P = G[:, :n-k]

    # H = [I_{n-k} | P.T]
    H = np.hstack((np.eye(n-k, dtype=np.uint8), P.T))

    return H


def create_syndrome_table(H):
    """
    Create a table of all possible syndromes and their corresponding error vectors (syndrome look-up table)
    
        @type  H: ndarray
        @param H: parity-check matrix
    """
    # Get the size of the parity-check matrix
    _, n = H.shape

    # Create a table of all possible syndromes and their corresponding error vectors (syndrome look-up table)
    coset_leader = np.vstack((np.zeros(n, dtype=np.uint8), np.eye(n, dtype=np.uint8)))
    possible_syndromes = (coset_leader @ H.T) % 2
    syndrome_table = {str(possible_syndromes[i]) : coset_leader[i] for i in range(n+1)}

    return syndrome_table



class Linear_Code:
    """
    (7, 4) Systematic Linear Block (Hamming) Code
    """
    def __init__(self):
        self.n, self.k = 7, 4
        self.G = np.array([[1, 1, 0, 1, 0, 0, 0],
                           [0, 1, 1, 0, 1, 0, 0],
                           [1, 1, 1, 0, 0, 1, 0],
                           [1, 0, 1, 0, 0, 0, 1]], dtype=np.uint8)
        self.H = np.array([[1, 0, 0, 1, 0, 1, 1],
                           [0, 1, 0, 1, 1, 1, 0],
                           [0, 0, 1, 0, 1, 1, 1]], dtype=np.uint8)
        self.syndrome_table = {'[0 0 0]' : np.array([0, 0, 0, 0, 0, 0, 0]),
                               '[1 0 0]' : np.array([1, 0, 0, 0, 0, 0, 0]),
                               '[0 1 0]' : np.array([0, 1, 0, 0, 0, 0, 0]),
                               '[0 0 1]' : np.array([0, 0, 1, 0, 0, 0, 0]),
                               '[1 1 0]' : np.array([0, 0, 0, 1, 0, 0, 0]),
                               '[0 1 1]' : np.array([0, 0, 0, 0, 1, 0, 0]),
                               '[1 1 1]' : np.array([0, 0, 0, 0, 0, 1, 0]),
                               '[1 0 1]' : np.array([0, 0, 0, 0, 0, 0, 1])}

    def encoder_systematic(self, bits):
        """
        Systematic - Encode the to-be-transmitted binary bits message with (7,4) hamming encoder, return the to-be-transmitted codewords

            @type  bits: ndarray
            @param bits: TX message

            @rtype:   ndarray
            @return:  TX codewords
        """
        encoded_array = np.zeros((len(bits) // self.k * self.n), dtype=np.uint8)

        for i in range(0, len(bits), self.k):
            message = bits[i:i + self.k]
            codeword = np.dot(message, self.G) % 2
            encoded_array[i // self.k * self.n:(i // self.k + 1) * self.n] = codeword

        return encoded_array


    def decoder_systematic(self, encoded_array):
        """
        Systematic - Decode the received binary bits codeword with (7,4) Hamming decoder, return the received message

            @type  encoded_array: ndarray
            @param encoded_array: RX codewords

            @rtype:   ndarray
            @return:  RX message
        """
        decoded_array = np.zeros((len(encoded_array) // self.n * self.k), dtype=np.uint8)

        err_count = 0

        for i in range(0, len(encoded_array), self.n):
            received_codeword = encoded_array[i:i + self.n]
            syndrome = np.dot(self.H, received_codeword) % 2
            if np.any(syndrome):  # If there are errors, count and keep it
                err_count += 1
            decoded_array[i // self.n * self.k : (i // self.n + 1) * self.k] = received_codeword[self.n - self.k:self.n]

        logger.info(f"Error codeword rate: {err_count/(len(encoded_array)//self.n)}")

        return decoded_array


    def corrector_syndrome(self, received_array):
        """
        Systematic - Correct the received binary bits codeword with (7,4) Hamming syndrome look-up table corrector, 
        return the estimated TX codeword = (RX codeword + error pattern)

            @type  received_array: ndarray
            @param received_array: RX codewords

            @rtype:   ndarray
            @return:  estimated TX codewords
        """
        corrected_array = received_array.copy()

        for i in range(0, len(received_array), self.n):
            received_codeword = received_array[i:i + self.n]
            syndrome = np.dot(self.H, received_codeword) % 2
            if np.any(syndrome):
                corrected_array[i:i + self.n] = (received_codeword + self.syndrome_table[str(syndrome)]) % 2

        return corrected_array



class Cyclic_Code(Linear_Code):
    """
    (n, k) Systematic Cyclic (Hamming) Code
    """
    def __init__(self, G):
        self.G = G
        self.k, self.n = self.G.shape
        self.H = create_parity_check_matrix(self.G)

        self.syndrome_table = create_syndrome_table(self.H)


    def corrector_lfsr(self, received_array):
        """
        Systematic - Correct the received binary bits codeword with (n, k) Hamming LFSR corrector,
        return the estimated TX codeword = (RX codeword + error pattern)

            @type  received_array: ndarray
            @param received_array: RX codewords

            @rtype:   ndarray
            @return:  estimated TX codewords
        """
        corrected_array = received_array.copy()
        pass


class Channel:
    """
    Channel
    """
    def binary_symmetric_channel(self, input_bits, p):
        """
        BSC - binary symmetric channel with adjustable error probability

            @type  input_bits: ndarray
            @param input_bits: TX codewords

            @type  p: float
            @param p: error_probability

            @rtype:   ndarray
            @return:  RX codewords
        """
        output_bits = np.copy(input_bits)
        for i in range(len(output_bits)):
            if np.random.random() < p:
                output_bits[i] = 1 - output_bits[i]  # flip the bit
        return output_bits



if __name__ == '__main__':
    # test
    tx_msg = np.array([0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1], dtype=np.uint8)
    print("Original bits:", tx_msg)

    # Channel
    channel = Channel()

    # Linear Code
    linear_code = Linear_Code()

    # Encoding
    tx_codewords = linear_code.encoder_systematic(tx_msg)
    print("Encoded bits      :", tx_codewords)

    # Passing through the channel
    rx_codewords = channel.binary_symmetric_channel(tx_codewords, 0.1)
    print("Bits after channel:", rx_codewords)

    # Correction with syndrome look-up table
    estimated_tx_codewords = linear_code.corrector_syndrome(rx_codewords)
    print("Estimated TX bits :", estimated_tx_codewords)

    # Decoding
    rx_msg = linear_code.decoder_systematic(estimated_tx_codewords)
    print("Decoded bits :", rx_msg)