# Copyright (c) 2023 Name

import logging

from Source import source
from Channel import channel
from Destination import destination


# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger in the main module
logger = logging.getLogger(__name__)




def error_correct_txt():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    txt    - hamming         - bsc     - hamming         - txt
    """
    src = source.Source()

    encoder = channel.Encoder()
    chl = channel.Channel()
    decoder = channel.Decoder()
    
    dest = destination.Destination()
    
    src.read_txt("Resource/hardcoded.txt")
    tx_msg = src.get_digital_data()

    tx_codeword = encoder.encoder_hamming(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    rx_msg = decoder.decoder_hamming(rx_codeword)

    dest.set_digital_data(rx_msg)
    dest.write_txt("Result/hamming-bsc-output.txt")


def error_correct_png():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    png    - hamming         - bsc     - hamming         - png
    """
    src = source.Source()

    encoder = channel.Encoder()
    chl = channel.Channel()
    decoder = channel.Decoder()
    
    dest = destination.Destination()
    
    height, width, channels = src.read_png("Resource/image.png")
    tx_msg = src.get_digital_data()

    tx_codeword = encoder.encoder_hamming(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    rx_msg = decoder.decoder_hamming(rx_codeword)

    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital("Result/hamming-bsc-output.png", height, width, channels)


if __name__ == '__main__':
    error_correct_txt()
    error_correct_png()