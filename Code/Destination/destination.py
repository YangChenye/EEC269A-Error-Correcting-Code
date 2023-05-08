# Copyright (c) 2023 Chenye Yang

import numpy as np
from PIL import Image
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


class Destination:
    """
    The destination
    """

    def set_digital_data(self, bits):
        """
        Record the received digital data

            @type  bits: ndarray
            @param bits: data bits
        """
        self._digital_data = bits


    def set_analogue_data(self, array):
        """
        Record the received analogue data

            @type  array: ndarray
            @param array: analogue data array
        """
        self._analogue_data = array


    def write_txt(self, dest_path):
        """
        Write data to a text file

            @type  dest_path: string
            @param dest_path: destination file path, with extension
        """
        byte_array = bytearray(np.packbits(self._digital_data).tobytes())
        with open(dest_path, 'wb') as file:
            file.write(byte_array)


    def write_png_from_digital(self, dest_path, height, width, channels):
        """
        Write color information in bits array to a png file

            @type  dest_path: string
            @param dest_path: destination file path, with extension

            @type  height: int
            @param height: height of the image

            @type  width: int
            @param width: width of the image

            @type  channels: int
            @param channels: channels of the image
        """
        # Convert the bit array to uint8 array
        uint8_array = np.packbits(self._digital_data)

        # Reshape the array to a 3D array of pixels (height, width, channels)
        pixels = uint8_array.reshape(height, width, channels)

        # Create a new image from the pixel values
        new_image = Image.fromarray(pixels)

        # Save the new image to a file
        new_image.save(dest_path)

    
    def write_png_from_analogue(self, dest_path):
        """
        Write color information in (height, width, channels) array to a png file

            @type  dest_path: string
            @param dest_path: destination file path, with extension
        """
        # Create a new image from the pixel values
        new_image = Image.fromarray(self._analogue_data)

        # Save the new image to a file
        new_image.save(dest_path)



if __name__ == '__main__':
    # test
    bits = np.array([0, 1, 0, 0, 1, 0, 0, 0]) # H
    destination = Destination()
    destination.set_data(bits)
    destination.write_file("output.txt")