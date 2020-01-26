import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq, ifft, rfft


def fft_from_data_frame(data_frame, fs, high=50000, low=30000):
    signal_set = []
    nan_indexes = np.where(np.any(np.isnan(data_frame.values), axis=1))
    data_frame_values = np.delete(data_frame.values, nan_indexes, axis=0)
    for row in data_frame_values:
        fft_data = fft(row, n=row.size)/row.size
        freq = fftfreq(row.size, d=1/fs)
        cut_high_signal = abs(fft_data).copy()
        cut_high_signal[(freq > high)] = 0
        cut_high_signal[(freq < low)] = 0
        signal_without_0 = list(filter(lambda a: a != 0, cut_high_signal))
        signal_set.append(np.abs(signal_without_0))
    return signal_set


def fft_chart_value(row, fs, high=50000, low=30000):
    fft_data = fft(row, n=row.size)/row.size
    freq = fftfreq(row.size, d=1/fs)
    cut_high_signal = abs(fft_data).copy()
    cut_high_signal[(freq > high)] = 0
    cut_high_signal[(freq < low)] = 0
    return freq, cut_high_signal
