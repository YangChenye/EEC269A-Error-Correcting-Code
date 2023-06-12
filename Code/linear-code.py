# Copyright (c) 2023 Chenye Yang

import logging
import os

import source
import channel
import destination
from Utils import plot_wav, stat_analysis


# Check if the directory exists
if not os.path.exists('Result/Linear/'):
    os.makedirs('Result/Linear/')

# Configure the logging
logging.basicConfig(filename='Result/Linear/logfile-linear.log',
                    filemode='w', # Overwrite the file
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger in the main module
logger = logging.getLogger(__name__)



def linear_txt():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    txt    - (7,4) linear    - bsc     - (7,4) linear    - txt
    """
    logger.info("***TXT***")
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    src.read_txt("Resource/hardcoded.txt")
    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # Statistic analysis
    correct_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 0, 7)
    one_error_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 1, 7)
    total_codewords = len(tx_codeword) // 7
    uncorrectable_codewords = total_codewords - correct_codewords - one_error_codewords
    logger.info("Channel statistic analysis:")
    logger.info("  Total codewords: %d", total_codewords)
    logger.info("  Correct codewords: %d", correct_codewords)
    logger.info("  Codeword error rate: %f", (total_codewords - correct_codewords) / total_codewords)
    logger.info("    One error codewords: %d", one_error_codewords)
    logger.info("    Uncorrectable codewords: %d", uncorrectable_codewords)

    # without error correction
    rx_msg = linear_code.decoder_systematic(rx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_txt("Result/Linear/linear-bsc-output.txt")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("Before correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))

    # with error correction
    estimated_tx_codeword = linear_code.corrector_syndrome(rx_codeword)
    rx_msg = linear_code.decoder_systematic(estimated_tx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_txt("Result/Linear/linear-bsc-output-syndrome-corrected.txt")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("After correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))


def linear_png():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    png    - (7,4) linear    - bsc     - (7,4) linear    - png
    """
    logger.info("***PNG***")
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    height, width, channels = src.read_png("Resource/image.png")
    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # Statistic analysis
    correct_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 0, 7)
    one_error_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 1, 7)
    total_codewords = len(tx_codeword) // 7
    uncorrectable_codewords = total_codewords - correct_codewords - one_error_codewords
    logger.info("Channel statistic analysis:")
    logger.info("  Total codewords: %d", total_codewords)
    logger.info("  Correct codewords: %d", correct_codewords)
    logger.info("  Codeword error rate: %f", (total_codewords - correct_codewords) / total_codewords)
    logger.info("    One error codewords: %d", one_error_codewords)
    logger.info("    Uncorrectable codewords: %d", uncorrectable_codewords)

    # without error correction
    rx_msg = linear_code.decoder_systematic(rx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital("Result/Linear/linear-bsc-output.png", height, width, channels)

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("Before correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))

    # with error correction
    estimated_tx_codeword = linear_code.corrector_syndrome(rx_codeword)
    rx_msg = linear_code.decoder_systematic(estimated_tx_codeword)
    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital("Result/Linear/linear-bsc-output-syndrome-corrected.png", height, width, channels)

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("After correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))


def linear_wav():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    wav    - (7,4) linear    - bsc     - (7,4) linear    - wav
    """
    logger.info("***WAV***")
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    shape, sample_rate = src.read_wav("Resource/file_example_WAV_1MG.wav")
    plot_wav.plot_wav_time_domain(src.get_analogue_data(), sample_rate, "Result/Linear/wav-time-domain-TX.png")
    plot_wav.plot_wav_frequency_domain(src.get_analogue_data(), sample_rate, "Result/Linear/wav-frequency-domain-TX.png")

    # tx_msg = src.get_analogue_data()
    # rx_msg = tx_msg
    # dest.set_analogue_data(rx_msg)
    # plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/Linear/wav-time-domain-RX.png")
    # plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/Linear/wav-frequency-domain-RX.png")
    # dest.write_wav_from_analogue(sample_rate, "Result/Linear/hamming-bsc-output.wav")


    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, 0.01)

    # Statistic analysis
    correct_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 0, 7)
    one_error_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 1, 7)
    total_codewords = len(tx_codeword) // 7
    uncorrectable_codewords = total_codewords - correct_codewords - one_error_codewords
    logger.info("Channel statistic analysis:")
    logger.info("  Total codewords: %d", total_codewords)
    logger.info("  Correct codewords: %d", correct_codewords)
    logger.info("  Codeword error rate: %f", (total_codewords - correct_codewords) / total_codewords)
    logger.info("    One error codewords: %d", one_error_codewords)
    logger.info("    Uncorrectable codewords: %d", uncorrectable_codewords)

    # without error correction
    rx_msg = linear_code.decoder_systematic(rx_codeword)

    dest.set_digital_data(rx_msg)
    dest.write_wav_from_digital(shape, sample_rate, "Result/Linear/linear-bsc-output.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/Linear/linear-bsc-wav-time-domain-RX.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/Linear/linear-bsc-wav-frequency-domain-RX.png")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("Before correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))

    # with error correction
    estimated_tx_codeword = linear_code.corrector_syndrome(rx_codeword)
    rx_msg = linear_code.decoder_systematic(estimated_tx_codeword)

    dest.set_digital_data(rx_msg)
    dest.write_wav_from_digital(shape, sample_rate, "Result/Linear/linear-bsc-output-syndrome-corrected.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/Linear/linear-bsc-wav-time-domain-RX-syndrome-corrected.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/Linear/linear-bsc-wav-frequency-domain-RX-syndrome-corrected.png")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("After correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))



if __name__ == '__main__':
    linear_txt()
    linear_png()
    linear_wav()