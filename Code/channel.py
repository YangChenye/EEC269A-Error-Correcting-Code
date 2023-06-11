# Copyright (c) 2023 Chenye Yang

import numpy as np
import logging

from Utils import polyTools

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
    syndrome_table = {tuple(possible_syndromes[i]) : coset_leader[i] for i in range(n+1)}

    return syndrome_table


def pad_bits(bits, k):
    """
    Pad the bits array with zeroes so its length is divisible by k.

        @type  bits: ndarray
        @param bits: TX message

        @type  k: int
        @param k: number of bits per codeword
    
    """
    padded_bits = bits.copy()
    remainder = len(bits) % k
    if remainder != 0:
        padding_length = k - remainder
        padded_bits = np.pad(padded_bits, (0, padding_length), mode='constant')
    return padded_bits


def remove_padding(bits, padding_length):
    """
    Remove the padding from the array.
    
        @type  bits: ndarray
        @param bits: RX message

        @type  padding_length: int
        @param padding_length: length of the original TX message
    """
    return bits[:-padding_length] if padding_length != 0 else bits



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
        self.syndrome_table = {
            (0, 0, 0): np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.uint8),
            (1, 0, 0): np.array([1, 0, 0, 0, 0, 0, 0], dtype=np.uint8),
            (0, 1, 0): np.array([0, 1, 0, 0, 0, 0, 0], dtype=np.uint8),
            (0, 0, 1): np.array([0, 0, 1, 0, 0, 0, 0], dtype=np.uint8),
            (1, 1, 0): np.array([0, 0, 0, 1, 0, 0, 0], dtype=np.uint8),
            (0, 1, 1): np.array([0, 0, 0, 0, 1, 0, 0], dtype=np.uint8),
            (1, 1, 1): np.array([0, 0, 0, 0, 0, 1, 0], dtype=np.uint8),
            (1, 0, 1): np.array([0, 0, 0, 0, 0, 0, 1], dtype=np.uint8),
            }


    def encoder_systematic(self, bits):
        """
        Systematic - Encode the to-be-transmitted binary bits message with (n,k) systematic encoder, pad with zero if not divisible, return the to-be-transmitted codewords

            @type  bits: ndarray
            @param bits: TX message

            @rtype:   ndarray
            @return:  TX codewords
        """
        # Pad the bits array with zeroes so its length is divisible by self.k
        padded_bits = pad_bits(bits, self.k)

        # Reshape the bits array to have one row per message
        messages = padded_bits.reshape(-1, self.k)

        # Perform the matrix multiplication operation in one go, and flatten the result to 1D array
        encoded_array = np.dot(messages, self.G) % 2

        # Flatten the array
        encoded_array = encoded_array.flatten()

        return encoded_array


    def decoder_systematic(self, encoded_array, padding_length=0):
        """
        Systematic - Decode the received binary bits codeword with (n,k) systematic decoder, remove padding, return the received message

            @type  encoded_array: ndarray
            @param encoded_array: RX codewords

            @type  padding_length: int
            @param padding_length: length of the padding (default: 0, means no padding)

            @rtype:   ndarray
            @return:  RX message
        """
        # Reshape the array so each row is a codeword
        reshaped_array = encoded_array.reshape(-1, self.n)

        # Compute the syndrome for each codeword
        syndromes = np.dot(reshaped_array, self.H.T) % 2

        # Count the number of non-zero syndromes (errors)
        err_count = np.count_nonzero(np.any(syndromes, axis=1))

        # Decode by taking the last self.k elements from each codeword
        decoded_array = reshaped_array[:, self.n - self.k:self.n].flatten()

        logger.debug(f"Error codeword rate: {err_count / (len(encoded_array) // self.n)}")

        # Remove the padding from the array
        if padding_length != 0:
            decoded_array = remove_padding(decoded_array, padding_length)

        return decoded_array


    def corrector_syndrome(self, received_array):
        """
        Systematic - Correct the received binary bits codeword with (n,k) Hamming syndrome look-up table corrector, 
        return the estimated TX codeword = (RX codeword + error pattern)

            @type  received_array: ndarray
            @param received_array: RX codewords

            @rtype:   ndarray
            @return:  estimated TX codewords
        """
        # Reshape the received_array so each row is a codeword
        reshaped_array = received_array.reshape(-1, self.n)

        # Compute the syndrome for each codeword
        syndromes = np.dot(reshaped_array, self.H.T) % 2

        # Copy reshaped_array to corrected_array for correction
        corrected_array = reshaped_array.copy()

        # Loop over the syndromes
        for i, syndrome in enumerate(syndromes):
            if np.any(syndrome):
                # Convert syndrome to tuple for lookup
                tuple_syndrome = tuple(syndrome)
                corrected_array[i] = (reshaped_array[i] + self.syndrome_table[tuple_syndrome]) % 2

        # Flatten corrected_array to match the shape of the input received_array
        corrected_array = corrected_array.flatten()

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
        # Generate a uniform random array of the same shape as input_bits
        random_numbers = np.random.rand(*input_bits.shape)
        
        # Identify where the random array is less than p
        mask = random_numbers < p
        
        # Use this mask to flip the bits at those indices
        output_bits = np.where(mask, 1 - input_bits, input_bits)

        return output_bits



if __name__ == '__main__':
    # test
    tx_msg = np.array([0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1], dtype=np.uint8)
    n = 7
    k = 4
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
    padding_length = k - (len(tx_msg) % k)
    rx_msg = linear_code.decoder_systematic(estimated_tx_codewords, padding_length)
    print("Decoded bits :", rx_msg)