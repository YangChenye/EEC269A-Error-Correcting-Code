# Copyright (c) 2023 Chenye Yang

import logging
import os

import source
import channel
import destination
from Utils import plot_wav, stat_analysis


''' 1st choose the code type '''
FLAG_SYSTEMATIC_HAMMING_LINEAR_CODE = True
FLAG_SYSTEMATIC_CYCLIC_CODE = True

''' 2nd choose the (n,k) and t correctable errors '''
# Linear Code is fixed (7,4)

# Cyclic Code:
# Encoder: (3, 1) (7, 4) (15, 11) (31, 26) (63, 57) cyclic hamming code (t=1)
# Decoder: Syndrome look-up table corrector | trapping corrector
# N, K = 127, 120
# FLAG_SYNDROME = True
# FLAG_TRAPPING = False

# Encoder: (15, 11, 1) (15, 7, 2) (15, 5, 3) (31, 26, 1) (31, 21, 2) (31, 16, 3) (31, 11, 5) (31, 6, 7) cyclic code
# Decoder: Trapping corrector
N, K = 31, 6
FLAG_SYNDROME = False
FLAG_TRAPPING = True

''' 3rd choose the channel '''
# BSC
ERROR_PROB = 0.01

''' 4th choose the source type '''
# TXT, PNG, WAV
FLAG_TXT = True
FLAG_PNG = True
FLAG_WAV = True

# choose one image
# PNG_PATH = "image.png"
PNG_PATH = "image2.png"
# PNG_PATH = "image3.png"
# PNG_PATH = "image4.png"







# Configure the logging
logging.basicConfig(filename='Result/Demo/logfile.log',
                    filemode='a', # Append the file
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger in the main module
logger = logging.getLogger(__name__)



if FLAG_SYSTEMATIC_HAMMING_LINEAR_CODE:
    # Check if the directory exists
    if not os.path.exists('Result/Demo/Linear/'):
        os.makedirs('Result/Demo/Linear/')

if FLAG_SYSTEMATIC_CYCLIC_CODE:
    # Check if the directory exists
    if not os.path.exists(f'Result/Demo/Cyclic/{N}-{K}/'):
        os.makedirs(f'Result/Demo/Cyclic/{N}-{K}/')




def linear_txt():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    txt    - (7,4) linear    - bsc     - (7,4) linear    - txt
    """
    logger.info("---------------TXT---------------")
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    src.read_txt("Resource/hardcoded.txt")
    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, ERROR_PROB)

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
    dest.write_txt("Result/Demo/Linear/linear-bsc-output.txt")

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
    dest.write_txt("Result/Demo/Linear/linear-bsc-output-syndrome-corrected.txt")

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
    logger.info("---------------PNG---------------")
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    height, width, channels = src.read_png(f"Resource/{PNG_PATH}")
    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, ERROR_PROB)

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
    dest.write_png_from_digital("Result/Demo/Linear/linear-bsc-output.png", height, width, channels)

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
    dest.write_png_from_digital("Result/Demo/Linear/linear-bsc-output-syndrome-corrected.png", height, width, channels)

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
    logger.info("---------------WAV---------------")
    src = source.Source()
    chl = channel.Channel()
    linear_code = channel.Linear_Code()
    dest = destination.Destination()


    shape, sample_rate = src.read_wav("Resource/file_example_WAV_1MG.wav")
    plot_wav.plot_wav_time_domain(src.get_analogue_data(), sample_rate, "Result/Demo/Linear/wav-time-domain-TX.png")
    plot_wav.plot_wav_frequency_domain(src.get_analogue_data(), sample_rate, "Result/Demo/Linear/wav-frequency-domain-TX.png")

    # tx_msg = src.get_analogue_data()
    # rx_msg = tx_msg
    # dest.set_analogue_data(rx_msg)
    # plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/Demo/Linear/wav-time-domain-RX.png")
    # plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/Demo/Linear/wav-frequency-domain-RX.png")
    # dest.write_wav_from_analogue(sample_rate, "Result/Demo/Linear/hamming-bsc-output.wav")


    tx_msg = src.get_digital_data()

    tx_codeword = linear_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, ERROR_PROB)

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
    dest.write_wav_from_digital(shape, sample_rate, "Result/Demo/Linear/linear-bsc-output.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/Demo/Linear/linear-bsc-wav-time-domain-RX.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/Demo/Linear/linear-bsc-wav-frequency-domain-RX.png")

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
    dest.write_wav_from_digital(shape, sample_rate, "Result/Demo/Linear/linear-bsc-output-syndrome-corrected.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/Demo/Linear/linear-bsc-wav-time-domain-RX-syndrome-corrected.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/Demo/Linear/linear-bsc-wav-frequency-domain-RX-syndrome-corrected.png")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("After correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))



def cyclic_txt():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    txt    - (n,k) cyclic    - bsc     - (n,k) cyclic    - txt
    """
    logger.info("---------------TXT---------------")
    src = source.Source()
    chl = channel.Channel()
    cyclic_code = channel.Cyclic_Code(N, K, None)
    dest = destination.Destination()


    src.read_txt("Resource/hardcoded.txt")
    tx_msg = src.get_digital_data()
    padding_length = (- len(tx_msg)) % K

    tx_codeword = cyclic_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, ERROR_PROB)

    # Statistic analysis
    correct_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 0, N)
    nECC = cyclic_code.nECC
    multiple_error_codewords = []
    for i in range(1, nECC+1):
        multiple_error_codewords.append(stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, i, N))
    total_codewords = len(tx_codeword) // N
    uncorrectable_codewords = total_codewords - correct_codewords - sum(multiple_error_codewords)
    logger.info("Channel statistic analysis:")
    logger.info("  Total codewords: %d", total_codewords)
    logger.info("  Correct codewords: %d", correct_codewords)
    logger.info("  Codeword error rate: %f", (total_codewords - correct_codewords) / total_codewords)
    for i in range(1, nECC+1):
        logger.info("    %d error codewords: %d", i, multiple_error_codewords[i-1])
    logger.info("    Uncorrectable codewords: %d", uncorrectable_codewords)

    # without error correction
    rx_msg = cyclic_code.decoder_systematic(rx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    dest.write_txt(f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output.txt")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("Before correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))

    # with error correction
    if FLAG_SYNDROME:
        estimated_tx_codeword = cyclic_code.corrector_syndrome(rx_codeword)
    elif FLAG_TRAPPING:
        estimated_tx_codeword = cyclic_code.corrector_trapping(rx_codeword)
    rx_msg = cyclic_code.decoder_systematic(estimated_tx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    if FLAG_SYNDROME:
        dest.write_txt(f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output-syndrome-corrected.txt")
    elif FLAG_TRAPPING:
        dest.write_txt(f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output-trapping-corrected.txt")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    if FLAG_SYNDROME:
        logger.info("After correction (syndrome):")
    elif FLAG_TRAPPING:
        logger.info("After correction (trapping):")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))


def cyclic_png():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    png    - (n,k) cyclic    - bsc     - (n,k) cyclic    - png
    """
    logger.info("---------------PNG---------------")
    src = source.Source()
    chl = channel.Channel()
    cyclic_code = channel.Cyclic_Code(N, K, None)
    dest = destination.Destination()


    height, width, channels = src.read_png(f"Resource/{PNG_PATH}")
    tx_msg = src.get_digital_data()
    padding_length = (- len(tx_msg)) % K

    tx_codeword = cyclic_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, ERROR_PROB)

    # Statistic analysis
    correct_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 0, N)
    nECC = cyclic_code.nECC
    multiple_error_codewords = []
    for i in range(1, nECC+1):
        multiple_error_codewords.append(stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, i, N))
    total_codewords = len(tx_codeword) // N
    uncorrectable_codewords = total_codewords - correct_codewords - sum(multiple_error_codewords)
    logger.info("Channel statistic analysis:")
    logger.info("  Total codewords: %d", total_codewords)
    logger.info("  Correct codewords: %d", correct_codewords)
    logger.info("  Codeword error rate: %f", (total_codewords - correct_codewords) / total_codewords)
    for i in range(1, nECC+1):
        logger.info("    %d error codewords: %d", i, multiple_error_codewords[i-1])
    logger.info("    Uncorrectable codewords: %d", uncorrectable_codewords)

    # without error correction
    rx_msg = cyclic_code.decoder_systematic(rx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    dest.write_png_from_digital(f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output.png", height, width, channels)

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("Before correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))

    # with error correction
    if FLAG_SYNDROME:
        estimated_tx_codeword = cyclic_code.corrector_syndrome(rx_codeword)
    elif FLAG_TRAPPING:
        estimated_tx_codeword = cyclic_code.corrector_trapping(rx_codeword)
    rx_msg = cyclic_code.decoder_systematic(estimated_tx_codeword, padding_length)
    dest.set_digital_data(rx_msg)
    if FLAG_SYNDROME:
        dest.write_png_from_digital(f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output-syndrome-corrected.png", height, width, channels)
    elif FLAG_TRAPPING:
        dest.write_png_from_digital(f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output-trapping-corrected.png", height, width, channels)

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    if FLAG_SYNDROME:
        logger.info("After correction (syndrome):")
    elif FLAG_TRAPPING:
        logger.info("After correction (trapping):")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))


def cyclic_wav():
    """
    Source - Channel encoder - Channel - Channel decoder - Destination

    wav    - (n,k) cyclic    - bsc     - (n,k) cyclic    - wav
    """
    logger.info("---------------WAV---------------")
    src = source.Source()
    chl = channel.Channel()
    cyclic_code = channel.Cyclic_Code(N, K, None)
    dest = destination.Destination()


    shape, sample_rate = src.read_wav("Resource/file_example_WAV_1MG.wav")
    plot_wav.plot_wav_time_domain(src.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/wav-time-domain-TX.png")
    plot_wav.plot_wav_frequency_domain(src.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/wav-frequency-domain-TX.png")

    # tx_msg = src.get_analogue_data()
    # rx_msg = tx_msg
    # dest.set_analogue_data(rx_msg)
    # plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, "Result/wav-time-domain-RX.png")
    # plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, "Result/wav-frequency-domain-RX.png")
    # dest.write_wav_from_analogue(sample_rate, "Result/hamming-bsc-output.wav")


    tx_msg = src.get_digital_data()
    padding_length = (- len(tx_msg)) % K

    tx_codeword = cyclic_code.encoder_systematic(tx_msg)

    rx_codeword = chl.binary_symmetric_channel(tx_codeword, ERROR_PROB)

    # Statistic analysis
    correct_codewords = stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, 0, N)
    nECC = cyclic_code.nECC
    multiple_error_codewords = []
    for i in range(1, nECC+1):
        multiple_error_codewords.append(stat_analysis.num_codeword_with_t_errors(tx_codeword, rx_codeword, i, N))
    total_codewords = len(tx_codeword) // N
    uncorrectable_codewords = total_codewords - correct_codewords - sum(multiple_error_codewords)
    logger.info("Channel statistic analysis:")
    logger.info("  Total codewords: %d", total_codewords)
    logger.info("  Correct codewords: %d", correct_codewords)
    logger.info("  Codeword error rate: %f", (total_codewords - correct_codewords) / total_codewords)
    for i in range(1, nECC+1):
        logger.info("    %d error codewords: %d", i, multiple_error_codewords[i-1])
    logger.info("    Uncorrectable codewords: %d", uncorrectable_codewords)

    # without error correction
    rx_msg = cyclic_code.decoder_systematic(rx_codeword, padding_length)

    dest.set_digital_data(rx_msg)
    dest.write_wav_from_digital(shape, sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output.wav")

    plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-wav-time-domain-RX.png")
    plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-wav-frequency-domain-RX.png")

    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    logger.info("Before correction:")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))

    # with error correction
    if FLAG_SYNDROME:
        estimated_tx_codeword = cyclic_code.corrector_syndrome(rx_codeword)
    elif FLAG_TRAPPING:
        estimated_tx_codeword = cyclic_code.corrector_trapping(rx_codeword)
    rx_msg = cyclic_code.decoder_systematic(estimated_tx_codeword, padding_length)

    dest.set_digital_data(rx_msg)
    if FLAG_SYNDROME:
        dest.write_wav_from_digital(shape, sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output-syndrome-corrected.wav")
        plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-wav-time-domain-RX-syndrome-corrected.png")
        plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-wav-frequency-domain-RX-syndrome-corrected.png")
    elif FLAG_TRAPPING:
        dest.write_wav_from_digital(shape, sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-output-trapping-corrected.wav")
        plot_wav.plot_wav_time_domain(dest.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-wav-time-domain-RX-trapping-corrected.png")
        plot_wav.plot_wav_frequency_domain(dest.get_analogue_data(), sample_rate, f"Result/Demo/Cyclic/{N}-{K}/cyclic-bsc-wav-frequency-domain-RX-trapping-corrected.png")


    # Statistic analysis
    correct_bits = stat_analysis.num_correct_bits(tx_msg, rx_msg)
    if FLAG_SYNDROME:
        logger.info("After correction (syndrome):")
    elif FLAG_TRAPPING:
        logger.info("After correction (trapping):")
    logger.info("  Number of correct bits: %d", correct_bits)
    logger.info("  Number of incorrect bits: %d", len(tx_msg) - correct_bits)
    logger.info("  Bit error rate: %f", (len(tx_msg) - correct_bits) / len(tx_msg))



if __name__ == '__main__':
    if FLAG_SYSTEMATIC_HAMMING_LINEAR_CODE:
        if FLAG_TXT:
            print("Linear: TXT")
            linear_txt()
        if FLAG_PNG:
            print("Linear: PNG")
            linear_png()
        if FLAG_WAV:
            print("Linear: WAV")
            linear_wav()

    if FLAG_SYSTEMATIC_CYCLIC_CODE:
        if FLAG_TXT:
            print("Cyclic: TXT")
            cyclic_txt()
        if FLAG_PNG:
            print("Cyclic: PNG")
            cyclic_png()
        if FLAG_WAV:
            print("Cyclic: WAV")
            cyclic_wav()