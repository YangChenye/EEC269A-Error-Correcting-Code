# Copyright (c) 2023 Chenye Yang

import numpy as np
from PIL import Image
from pydub import AudioSegment
from scipy.io import wavfile
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


    def get_digital_data(self):
        """
        Get the received digital data

            @rtype:   ndarray
            @return:  data bits
        """
        return self._digital_data


    def get_analogue_data(self):
        """
        Get the received analogue data

            @rtype:   ndarray
            @return:  analogue data
        """
        return self._analogue_data


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
        Write color information in bits array to a png file, at the same time store the color information as ndarray in _analogue_data

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

        # Store the analogue data
        self._analogue_data = pixels

        # Create a new image from the pixel values
        new_image = Image.fromarray(pixels)

        # Save the new image to a file
        new_image.save(dest_path)

    
    def write_png_from_analogue(self, dest_path):
        """
        Write color information in (height, width, channels) array to a png file, at the same time store the color information as bit array in _digital_data

            @type  dest_path: string
            @param dest_path: destination file path, with extension
        """
        # Create a new image from the pixel values
        new_image = Image.fromarray(self._analogue_data)

        # Save the new image to a file
        new_image.save(dest_path)

        # Convert the img_array to binary format and flatten the array
        bits = np.unpackbits(self._analogue_data.astype(np.uint8)).flatten()

        # Store the binary bits
        self._digital_data = bits


    def write_wav_from_digital(self, shape, sample_rate, dest_path):
        """
        Write audio information in bits array to a wav file, at the same time store the audio information as ndarray in _analogue_data

            @type  dest_path: string
            @param dest_path: destination file path, with extension
        """
        # Convert the bit array to uint16 array
        uint16_array = np.packbits(self._digital_data).astype(np.int16)

        # Reshape the array to a 2D array of samples (channels, samples)
        audio_array = uint16_array.reshape(shape)

        # Store the analogue data
        self._analogue_data = audio_array

        # Write the array to a wav file
        wavfile.write(dest_path, sample_rate, audio_array)

    
    def write_wav_from_analogue(self, sample_rate, dest_path):
        """
        Write audio information in audio array to a wav file, at the same time store the audio information as bit array in _digital_data

            @type  dest_path: string
            @param dest_path: destination file path, with extension
        """
        # Write the array to a wav file
        wavfile.write(dest_path, sample_rate, self._analogue_data)

        # Convert the audio_array to binary format and flatten the array
        bits = np.unpackbits(self._analogue_data.astype(np.uint8)).flatten()

        # Store the binary bits
        self._digital_data = bits


    # def write_mp3_from_digital(self, frame_rate, sample_width, channels, dest_path):
    #     """
    #     Write audio information in bits array to a mp3 file

    #         @type  dest_path: string
    #         @param dest_path: destination file path, with extension
    #     """
    #     # Convert the bit array to uint16 array
    #     uint16_array = np.packbits(self._digital_data).astype(np.int16)

    #     # Create a new AudioSegment object from the modified audio array
    #     modified_audio = AudioSegment(uint16_array.tobytes(), frame_rate, sample_width, channels)

    #     # Export the modified audio to a new MP3 file
    #     modified_audio.export(dest_path, format="mp3")


    # def write_mp3_from_analogue(self, frame_rate, sample_width, channels, dest_path):
    #     """
    #     Write audio information in audio array to a mp3 file

    #         @type  dest_path: string
    #         @param dest_path: destination file path, with extension
    #     """
    #     # Create a new AudioSegment object from the modified audio array
    #     modified_audio = AudioSegment(self._analogue_data.tobytes(), frame_rate, sample_width, channels)

    #     # Export the modified audio to a new MP3 file
    #     modified_audio.export(dest_path, format="mp3")



if __name__ == '__main__':
    # test
    bits = np.array([0, 1, 0, 0, 1, 0, 0, 0]) # H
    destination = Destination()
    destination.set_data(bits)
    destination.write_file("output.txt")