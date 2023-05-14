# Copyright (c) 2023 Chenye Yang

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import logging

# Create a logger in this module
logger = logging.getLogger(__name__)


def plot_mp3_time_domain(audio_array, frame_rate, dest_path):
    """
    Plot the audio signal in the time domain.
    
        @type  audio_array: ndarray
        @param audio_array: audio data array

        @type  frame_rate: int
        @param frame_rate: frame rate of the audio

        @type  dest_path: string
        @param dest_path: destination file path, with extension
    """
    # Generate the time axis
    duration = len(audio_array) / frame_rate
    time = np.linspace(0., duration, len(audio_array))

    # Plot the audio signal in the time domain
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio_array)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Audio Signal in the Time Domain")
    plt.savefig(dest_path, dpi=300)
    plt.close()


def plot_mp3_frequency_domain(audio_array, frame_rate, dest_path):
    """
    Plot the audio signal in the frequency domain.
        
        @type  audio_array: ndarray
        @param audio_array: audio data array

        @type  frame_rate: int
        @param frame_rate: frame rate of the audio

        @type  dest_path: string
        @param dest_path: destination file path, with extension
    """
    # Compute the spectrogram of the audio
    frequencies, times, spectrogram = signal.spectrogram(audio_array, frame_rate)

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram))
    plt.colorbar(label='Power Spectral Density (dB/Hz)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram of the Audio Signal')
    plt.savefig(dest_path, dpi=300)
    plt.close()
