# Copyright (c) 2023 Chenye Yang

import numpy as np
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


class Source:
    """
    The data source
    """

    def read_file(self, src_path):
        """
        Read the file as binary bits

            @type  src_path: string
            @param src_path: source file path, with extension
        """
        with open(src_path, 'rb') as file:
            byte_array = bytearray(file.read())
            self._data = np.unpackbits(np.frombuffer(byte_array, dtype=np.uint8))


    def get_data(self):
        """
        Get the bits to be transmitted

            @rtype:   ndarray
            @return:  data bits
        """
        return self._data
    

if __name__ == '__main__':
    # test
    source = Source()
    source.read_file("Resource/hardcoded.txt")
    bits = source.get_data()
    print(bits)
    print(type(bits))