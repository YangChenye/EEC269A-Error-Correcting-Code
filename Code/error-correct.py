# Copyright (c) 2023 Name

import logging

from Source import source
from Channel import channel
from Destination import destination


# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger in the main module
logger = logging.getLogger(__name__)




def error_correct():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination
    """
    data_src = source.Source()
    # data_chl = channel.Channel()
    data_dest = destination.Destination()
    
    data_src.read_file("Resource/image.jpg")
    bits = data_src.get_data()

    data_dest.set_data(bits)
    data_dest.write_file("Result/output.jpg")




if __name__ == '__main__':
    error_correct()