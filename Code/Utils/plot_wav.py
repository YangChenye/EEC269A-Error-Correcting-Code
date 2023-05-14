# Copyright (c) 2023 Chenye Yang

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft


def plot_wav_time_domain(audio_array, sample_rate, dest_path):
    """
    Plot the audio signal in the time domain.
    
        @type  audio_array: ndarray
        @param audio_array: audio data array

        @type  sample_rate: int
        @param sample_rate: sample rate of the audio

        @type  dest_path: string
        @param dest_path: destination file path, with extension
    """
    # Copy the audio array
    data = audio_array.copy()
    # Normalize to [-1, 1]
    data = data / np.max(np.abs(data),axis=0)

    times = np.arange(len(data))/float(sample_rate)

    # Prepare the subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))

    # Time domain representation for channel 1
    axs[0].fill_between(times, data[:, 0], color='k') 
    axs[0].set_xlim(times[0], times[-1])
    axs[0].set_xlabel('time (s)')
    axs[0].set_ylabel('amplitude')
    axs[0].set_title('Time Domain Representation - Channel 1')

    # Time domain representation for channel 2
    axs[1].fill_between(times, data[:, 1], color='k') 
    axs[1].set_xlim(times[0], times[-1])
    axs[1].set_xlabel('time (s)')
    axs[1].set_ylabel('amplitude')
    axs[1].set_title('Time Domain Representation - Channel 2')

    # Display the plot
    plt.tight_layout()
    plt.savefig(dest_path, dpi=300)
    plt.close()


def plot_wav_frequency_domain(audio_array, sample_rate, dest_path):
    """
    Plot the audio signal in the frequency domain.

        @type  audio_array: ndarray
        @param audio_array: audio data array

        @type  sample_rate: int
        @param sample_rate: sample rate of the audio

        @type  dest_path: string
        @param dest_path: destination file path, with extension
    """
    # Copy the audio array
    data = audio_array.copy()
    # Normalize to [-1, 1]
    data = data / np.max(np.abs(data),axis=0)

    # Prepare the subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))

    # Frequency domain representation for channel 1
    fft_out_channel_1 = fft(data[:, 0])
    magnitude_spectrum_channel_1 = np.abs(fft_out_channel_1)
    frequencies_channel_1 = np.linspace(0, sample_rate, len(magnitude_spectrum_channel_1))

    axs[0].plot(frequencies_channel_1[:int(len(frequencies_channel_1)/2)], magnitude_spectrum_channel_1[:int(len(magnitude_spectrum_channel_1)/2)]) # plot only first half of frequencies
    axs[0].set_xlabel('frequency (Hz)')
    axs[0].set_ylabel('magnitude')
    axs[0].set_title('Frequency Domain Representation - Channel 1')

    # Frequency domain representation for channel 2
    fft_out_channel_2 = fft(data[:, 1])
    magnitude_spectrum_channel_2 = np.abs(fft_out_channel_2)
    frequencies_channel_2 = np.linspace(0, sample_rate, len(magnitude_spectrum_channel_2))

    axs[1].plot(frequencies_channel_2[:int(len(frequencies_channel_2)/2)], magnitude_spectrum_channel_2[:int(len(magnitude_spectrum_channel_2)/2)]) # plot only first half of frequencies
    axs[1].set_xlabel('frequency (Hz)')
    axs[1].set_ylabel('magnitude')
    axs[1].set_title('Frequency Domain Representation - Channel 2')

    # Display the plot
    plt.tight_layout()
    plt.savefig(dest_path, dpi=300)
    plt.close()
