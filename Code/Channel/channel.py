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
        self.G = np.array([[1, 0, 0, 0, 1, 0, 1],
                           [0, 1, 0, 0, 1, 1, 1],
                           [0, 0, 1, 0, 1, 1, 0],
                           [0, 0, 0, 1, 0, 1, 1]], dtype=np.uint8)
        self.H = np.array([[1, 1, 1, 0, 1, 0, 0],
                           [0, 1, 1, 1, 0, 1, 0],
                           [1, 1, 0, 1, 0, 0, 1]], dtype=np.uint8)

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
        self.G = np.array([[1, 0, 0, 0, 1, 0, 1],
                           [0, 1, 0, 0, 1, 1, 1],
                           [0, 0, 1, 0, 1, 1, 0],
                           [0, 0, 0, 1, 0, 1, 1]], dtype=np.uint8)
        self.H = np.array([[1, 1, 1, 0, 1, 0, 0],
                           [0, 1, 1, 1, 0, 1, 0],
                           [1, 1, 0, 1, 0, 0, 1]], dtype=np.uint8)
        
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
            decoded_array[i // self.n * self.k : (i // self.n + 1) * self.k] = received_codeword[:self.k]

        logger.info(f"Error codeword rate: {self.err_count/(len(encoded_array)//self.n)}")
        self.err_count = 0

        return decoded_array


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
    rx_codewords = channel.binary_symmetric_channel(tx_codewords, 0.5)
    print("Bits after channel:", rx_codewords)

    # Decoding
    decoder = Decoder()
    rx_msg = decoder.decoder_hamming(rx_codewords)
    print("Decoded bits :", rx_msg)