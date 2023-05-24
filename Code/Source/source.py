# Copyright (c) 2023 Chenye Yang

import numpy as np
from PIL import Image
import soundfile as sf
# from scipy.io import wavfile
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
        bits = np.unpackbits(img_array.astype(np.uint8))

        # Store the binary bits
        self._digital_data = bits
        # Store the analogue data
        self._analogue_data = img_array

        return height, width, channels
    

    def read_wav(self, src_path):
        """
        Read the wav file, 
        store the audio information as binary bits in _digital_data, 
        store the audio information as ndarray in _analogue_data. 
        Return the frame_rate, sample_width, channels of the audio.

            @type  src_path: string
            @param src_path: source file path, with extension

            @rtype:   tuple
            @return:  frame rate, sample width, channels
        """
        # Open the audio file
        # sample_rate, audio_array = wavfile.read(src_path)
        audio_array, sample_rate = sf.read(src_path, dtype='int16')
        shape = audio_array.shape

        # Convert the audio_array to binary format and flatten the array
        bits = np.unpackbits(audio_array.astype(np.int16).view(np.uint8))

        # Store the binary bits
        self._digital_data = bits
        # Store the analogue data
        self._analogue_data = audio_array

        return shape, sample_rate
    

    # def read_mp3(self, src_path):
    #     """
    #     Read the mp3 file,
    #     store the audio information as binary bits in _digital_data, 
    #     store the audio information as ndarray in _analogue_data. 
    #     Return the frame_rate, sample_width, channels of the audio.

    #         @type  src_path: string
    #         @param src_path: source file path, with extension

    #         @rtype:   tuple
    #         @return:  frame rate, sample width, channels
    #     """
    #     # Open the audio file
    #     audio = AudioSegment.from_file(src_path, format="mp3")
    #     frame_rate, sample_width, channels = audio.frame_rate, audio.sample_width, audio.channels

    #     # Convert the audio to a NumPy array
    #     audio_array = np.array(audio.get_array_of_samples())
    #     # print(audio_array.dtype)

    #     # Get the shape of the array: e.g. (2392270,)
    #     # shape = audio_array.shape

    #     # Convert the audio_array to binary format and flatten the array
    #     bits = np.unpackbits(audio_array.astype(np.uint8))

    #     # Store the binary bits
    #     self._digital_data = bits
    #     # Store the analogue data
    #     self._analogue_data = audio_array

    #     return frame_rate, sample_width, channels



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
    text_bits = source.get_digital_data()
    print(text_bits)
    print(type(text_bits))

    source.read_png("Resource/image.png")
    image_bits = source.get_digital_data()
    print(image_bits[:16])
    image_pixels = source.get_analogue_data()
    print(image_pixels[0][0][:2])

    # frame_rate, sample_width, channels = source.read_mp3("Resource/file_example_MP3_1MG.mp3")
    # print(frame_rate, sample_width, channels)
    # audio_bits = source.get_digital_data()
    # print(audio_bits[:16])
    # audio_array = source.get_analogue_data()
    # print(audio_array[:2])

    source.read_wav("Resource/file_example_WAV_1MG.wav")
    audio_bits = source.get_digital_data()
    print(audio_bits[:16])
    audio_array = source.get_analogue_data()
    print(audio_array[:2])