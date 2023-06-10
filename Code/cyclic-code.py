# Copyright (c) 2023 Chenye Yang

import logging

import source
import channel
import destination
from Utils import plot_wav, polyTools


# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger in the main module
logger = logging.getLogger(__name__)



# Work with (3, 1) (7, 4) (15, 11) (31, 26) (63, 57) (127, 120) (255, 247) (511, 502) cyclic hamming code
(n, k) = (31, 26)

# Create the generator matrix
genMatrix_decimal = polyTools.findMatrix(n, k)
G = polyTools.genMatrixDecmial2Ndarray(genMatrix_decimal, n)


def cyclic_txt():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    txt    - (n,k) cyclic    - bsc     - (n,k) cyclic    - txt
    """
    src = source.Source()
    chl = channel.Channel()
    cyclic_code = channel.Cyclic_Code(G)
    dest = destination.Destination()


    src.read_txt("Resource/hardcoded.txt")
    tx_msg = src.get_digital_data()
    padding_length = k - (len(tx_msg) % k)

    tx_codeword = cyclic_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # without error correction
    rx_msg = cyclic_code.decoder_systematic(rx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    dest.write_txt("Result/cyclic-bsc-output.txt")

    # with error correction
    estimated_tx_codeword = cyclic_code.corrector_syndrome(rx_codeword)
    rx_msg = cyclic_code.decoder_systematic(estimated_tx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    dest.write_txt("Result/cyclic-bsc-output-syndrome-corrected.txt")


def cyclic_png():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    png    - (n,k) cyclic    - bsc     - (n,k) cyclic    - png
    """
    src = source.Source()
    chl = channel.Channel()
    cyclic_code = channel.Cyclic_Code(G)
    dest = destination.Destination()


    height, width, channels = src.read_png("Resource/image.png")
    tx_msg = src.get_digital_data()
    padding_length = k - (len(tx_msg) % k)

    tx_codeword = cyclic_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # without error correction
    rx_msg = cyclic_code.decoder_systematic(rx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital("Result/cyclic-bsc-output.png", height, width, channels)

    # with error correction
    estimated_tx_codeword = cyclic_code.corrector_syndrome(rx_codeword)
    rx_msg = cyclic_code.decoder_systematic(estimated_tx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital("Result/cyclic-bsc-output-syndrome-corrected.png", height, width, channels)


def cyclic_wav():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    wav    - (n,k) cyclic    - bsc     - (n,k) cyclic    - wav
    """
    src = source.Source()
    chl = channel.Channel()
    cyclic_code = channel.Cyclic_Code(G)
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
    padding_length = k - (len(tx_msg) % k)

    tx_codeword = cyclic_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # without error correction
    rx_msg = cyclic_code.decoder_systematic(rx_codeword, padding_length)

    dest.set_digital_data(rx_msg)
    dest.write_wav_from_digital(shape, sample_rate, "Result/cyclic-bsc-output.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/cyclic-bsc-wav-time-domain-RX.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/cyclic-bsc-wav-frequency-domain-RX.png")

    # with error correction
    estimated_tx_codeword = cyclic_code.corrector_syndrome(rx_codeword)
    rx_msg = cyclic_code.decoder_systematic(estimated_tx_codeword, padding_length)

    dest.set_digital_data(rx_msg)
    dest.write_wav_from_digital(shape, sample_rate, "Result/cyclic-bsc-output-syndrome-corrected.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/cyclic-bsc-wav-time-domain-RX-syndrome-corrected.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/cyclic-bsc-wav-frequency-domain-RX-syndrome-corrected.png")


if __name__ == '__main__':
    cyclic_txt()
    cyclic_png()
    cyclic_wav()