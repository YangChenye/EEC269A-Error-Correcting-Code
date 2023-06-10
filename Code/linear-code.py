# Copyright (c) 2023 Chenye Yang

import logging

import source
import channel
import destination
from Utils import plot_wav


# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger in the main module
logger = logging.getLogger(__name__)



def linear_txt():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    txt    - (7,4) linear    - bsc     - (7,4) linear    - txt
    """
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    src.read_txt("Resource/hardcoded.txt")
    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # without error correction
    rx_msg = linear_code.decoder_systematic(rx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_txt("Result/linear-bsc-output.txt")

    # with error correction
    estimated_tx_codeword = linear_code.corrector_syndrome(rx_codeword)
    rx_msg = linear_code.decoder_systematic(estimated_tx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_txt("Result/linear-bsc-output-syndrome-corrected.txt")


def linear_png():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    png    - (7,4) linear    - bsc     - (7,4) linear    - png
    """
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    height, width, channels = src.read_png("Resource/image.png")
    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # without error correction
    rx_msg = linear_code.decoder_systematic(rx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital("Result/linear-bsc-output.png", height, width, channels)

    # with error correction
    estimated_tx_codeword = linear_code.corrector_syndrome(rx_codeword)
    rx_msg = linear_code.decoder_systematic(estimated_tx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital("Result/linear-bsc-output-syndrome-corrected.png", height, width, channels)


def linear_wav():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    wav    - (7,4) linear    - bsc     - (7,4) linear    - wav
    """
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
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

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # without error correction
    rx_msg = linear_code.decoder_systematic(rx_codeword)

    dest.set_digital_data(rx_msg)
    dest.write_wav_from_digital(shape, sample_rate, "Result/linear-bsc-output.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/linear-bsc-wav-time-domain-RX.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/linear-bsc-wav-frequency-domain-RX.png")

    # with error correction
    estimated_tx_codeword = linear_code.corrector_syndrome(rx_codeword)
    rx_msg = linear_code.decoder_systematic(estimated_tx_codeword)

    dest.set_digital_data(rx_msg)
    dest.write_wav_from_digital(shape, sample_rate, "Result/linear-bsc-output-syndrome-corrected.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/linear-bsc-wav-time-domain-RX-syndrome-corrected.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/linear-bsc-wav-frequency-domain-RX-syndrome-corrected.png")


if __name__ == '__main__':
    linear_txt()
    linear_png()
    linear_wav()