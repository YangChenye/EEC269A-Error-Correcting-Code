# Copyright (c) 2023 Name

import numpy as np
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


class Encoder:
    """
    Channel encoder

        @type  variable: type
        @param variable: description
    """
    def __init__(self):
        self.n, self.k = 7, 4
        self.G = np.array([[1, 0, 0, 0, 1, 0, 1],
                      [0, 1, 0, 0, 1, 1, 1],
                      [0, 0, 1, 0, 1, 1, 0],
                      [0, 0, 0, 1, 0, 1, 1]], dtype=int)
        self.H = np.array([[1, 1, 1, 0, 1, 0, 0],
                      [1, 1, 0, 1, 0, 1, 0],
                      [1, 0, 1, 1, 0, 0, 1]], dtype=int)

    def encoder_hamming(self, bits):
        """
        Encode the binary bits data with (7,4) hamming encoder

            @type  bits: bits string
            @param bits: data

            @rtype:   return typr
            @return:  description
        """
        pass
    

if __name__ == '__main__':
    # test your function here
    pass