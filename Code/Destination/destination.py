# Copyright (c) 2023 Chenye Yang

import numpy as np
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


class Destination:
    """
    The destination
    """

    def set_data(self, bits):
        """
        Record the received data

            @type  bits: ndarray
            @param bits: data bits
        """
        self._data = bits


    def write_file(self, dest_path):
        """
        Write data to a file

            @type  dest_path: string
            @param dest_path: destination file path, with extension
        """
        byte_array = bytearray(np.packbits(self._data).tobytes())
        with open(dest_path, 'wb') as file:
            file.write(byte_array)
    

if __name__ == '__main__':
    # test
    bits = np.array([0, 1, 0, 0, 1, 0, 0, 0]) # H
    destination = Destination()
    destination.set_data(bits)
    destination.write_file("output.txt")