# Copyright (c) 2023 Name

import logging

from PIL import Image
import io



# Create a logger in this module
logger = logging.getLogger(__name__)


class Source:
    """
    Description of class and constructor here

        @type  variable: src_type
        @param variable: description
    """
    def __init__(self, src_type, src_path):
        self.src_type = src_type
        self.src_path = src_path

        self._read_data()

        


    def _read_data(self):
        """
        Read the data to be transmited from a file with given path
        """
        match self.src_type:
            case "hardcoded":
                # Open the file in binary mode for reading ('rb')
                with open(self.src_path, 'rb') as file:
                    # Read the file contents into a bytes object
                    self.data = file.read()

            case "image":
                # Open the image
                img = Image.open(self.src_path)

                # Convert the image to bytes
                byte_stream = io.BytesIO()
                img.save(byte_stream, format='JPEG')  # Change the format if needed (e.g., 'PNG')
                byte_stream.seek(0)  # Reset the stream position to the beginning
                self.data = byte_stream.read()


            case "audio":
                pass


    def func(self, variable):
        """
        Description of function

            @type  variable: type
            @param variable: description

            @rtype:   return typr
            @return:  description
        """
        return variable
    

if __name__ == '__main__':
    # test your function here
    pass