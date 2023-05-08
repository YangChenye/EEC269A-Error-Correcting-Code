# Copyright (c) 2023 Chenye Yang

import numpy as np
from PIL import Image
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


class Source:
    """
    The data source
    """

    def read_txt(self, src_path):
        """
        Read the text file as binary bits

            @type  src_path: string
            @param src_path: source file path, with extension
        """
        with open(src_path, 'rb') as file:
            byte_array = bytearray(file.read())
            self._digital_data = np.unpackbits(np.frombuffer(byte_array, dtype=np.uint8))


    def read_png(self, src_path):
        """
        Read the png file, 
        store the color information as binary bits in _digital_data, 
        store the color information as ndarray in _analogue_data. 
        Return the height, width, channels of the image.

            @type  src_path: string
            @param src_path: source file path, with extension

            @rtype:   tuple
            @return:  height, width, channels
        """
        # Open the image file
        image = Image.open(src_path)

        # Convert the image to a NumPy array
        img_array = np.array(image)

        # Get the shape of the array (height, width, channels)
        height, width, channels = img_array.shape

        # Convert the img_array to binary format and flatten the array
        bits = np.unpackbits(img_array.astype(np.uint8)).flatten()

        # Store the binary bits
        self._digital_data = bits
        # Store the analogue data
        self._analogue_data = img_array

        return height, width, channels



    def get_digital_data(self):
        """
        Get the bits to be transmitted

            @rtype:   ndarray
            @return:  data bits
        """
        return self._digital_data
    

    def get_analogue_data(self):
        """
        Get the analogue data to be transmitted

            @rtype:   ndarray
            @return:  analogue data
        """
        return self._analogue_data
    

if __name__ == '__main__':
    # test
    source = Source()
    source.read_txt("Resource/hardcoded.txt")
    bits = source.get_digital_data()
    print(bits)
    print(type(bits))

    source.read_png("Resource/image.png")
    bits = source.get_digital_data()
    print(bits[:16])
    pixels = source.get_analogue_data()
    print(pixels[0][0][:2])