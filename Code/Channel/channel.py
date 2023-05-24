# Copyright (c) 2023 Name

import numpy as np
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


class Encoder:
    """
    Channel encoder
    """
    def __init__(self):
        # Hamming code
        self.n, self.k = 7, 4
        self.G = np.array([[1, 1, 0, 1, 0, 0, 0],
                           [0, 1, 1, 0, 1, 0, 0],
                           [1, 1, 1, 0, 0, 1, 0],
                           [1, 0, 1, 0, 0, 0, 1]], dtype=np.uint8)
        self.H = np.array([[1, 0, 0, 1, 0, 1, 1],
                           [0, 1, 0, 1, 1, 1, 0],
                           [0, 0, 1, 0, 1, 1, 1]], dtype=np.uint8)

    def encoder_hamming(self, bits):
        """
        Hamming - Encode the to-be-transmitted binary bits message with (7,4) hamming encoder, return the to-be-transmitted codewords

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



class Decoder:
    """
    Channel decoder
    """
    def __init__(self):
        # Hamming code
        self.n, self.k = 7, 4
        self.G = np.array([[1, 1, 0, 1, 0, 0, 0],
                           [0, 1, 1, 0, 1, 0, 0],
                           [1, 1, 1, 0, 0, 1, 0],
                           [1, 0, 1, 0, 0, 0, 1]], dtype=np.uint8)
        self.H = np.array([[1, 0, 0, 1, 0, 1, 1],
                           [0, 1, 0, 1, 1, 1, 0],
                           [0, 0, 1, 0, 1, 1, 1]], dtype=np.uint8)

        self.err_count = 0


    def decoder_hamming(self, encoded_array):
        """
        Hamming - Decode the received binary bits codeword with (7,4) Hamming decoder, return the received message

            @type  encoded_array: ndarray
            @param encoded_array: RX codewords

            @rtype:   ndarray
            @return:  RX message
        """
        decoded_array = np.zeros((len(encoded_array) // self.n * self.k), dtype=np.uint8)

        for i in range(0, len(encoded_array), self.n):
            received_codeword = encoded_array[i:i + self.n]
            syndrome = np.dot(self.H, received_codeword) % 2
            if np.any(syndrome):  # If there are errors, count and keep it
                self.err_count += 1
            decoded_array[i // self.n * self.k : (i // self.n + 1) * self.k] = received_codeword[self.n - self.k:self.n]

        logger.info(f"Error codeword rate: {self.err_count/(len(encoded_array)//self.n)}")
        self.err_count = 0

        return decoded_array



class Error_Corrector:
    """
    Channel error corrector
    """
    def __init__(self):
        # Hamming code
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
        
        self.err_count = 0


    def corrector_hamming_syndrome(self, received_array):
        """
        Hamming - Correct the received binary bits codeword with (7,4) Hamming syndrome look-up table corrector, 
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

    # Encoding
    encoder = Encoder()
    tx_codewords = encoder.encoder_hamming(tx_msg)
    print("Encoded bits      :", tx_codewords)

    # Channel
    channel = Channel()
    rx_codewords = channel.binary_symmetric_channel(tx_codewords, 0.1)
    print("Bits after channel:", rx_codewords)

    # Correction
    corrector = Error_Corrector()
    estimated_tx_codewords = corrector.corrector_hamming_syndrome(rx_codewords)
    print("Estimated TX bits :", estimated_tx_codewords)

    # Decoding
    decoder = Decoder()
    rx_msg = decoder.decoder_hamming(estimated_tx_codewords)
    print("Decoded bits :", rx_msg)