# Copyright (c) 2023 Name

import logging

from Source import source
from Channel import channel
from Destination import destination
from Utils import plot_wav


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


def error_correct_wav():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    wav    - hamming         - bsc     - hamming         - wav
    """
    src = source.Source()

    encoder = channel.Encoder()
    chl = channel.Channel()
    decoder = channel.Decoder()
    
    dest = destination.Destination()
    
    shape, sample_rate = src.read_wav("Resource/file_example_WAV_1MG.wav")
    plot_wav.plot_wav_time_domain(src.get_analogue_data(), sample_rate, "Result/wav-time-domain-TX.png")
    plot_wav.plot_wav_frequency_domain(src.get_analogue_data(), sample_rate, "Result/wav-frequency-domain-TX.png")

    # tx_msg = src.get_analogue_data()

    # rx_msg = tx_msg

    # dest.set_analogue_data(rx_msg)

    # plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/wav-time-domain-RX.png")
    # plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/wav-frequency-domain-RX.png")

    # dest.write_wav_from_analogue(sample_rate, "Result/hamming-bsc-output.wav")
    

    tx_msg = src.get_digital_data()

    tx_codeword = encoder.encoder_hamming(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    rx_msg = decoder.decoder_hamming(rx_codeword)

    dest.set_digital_data(rx_msg)

    dest.write_wav_from_digital(shape, sample_rate, "Result/hamming-bsc-output.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/wav-time-domain-RX.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/wav-frequency-domain-RX.png")


if __name__ == '__main__':
    # error_correct_txt()
    # error_correct_png()
    error_correct_wav()