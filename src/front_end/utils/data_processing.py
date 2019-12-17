import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import butter, lfilter, freqz
from scipy import signal
data_after_applying_filter = []

cutoff_low = 60000  # in Hz
cutoff_high = 30000
fs = 1.14*1e6  # 5 micro samples per second
order = 5
NOISE_SIZE = 350
DATA_HEADERS_SIZE = 9
ECHO_SIZE_LEFT = 356
ECHO_SIZE_RIGHT = 1024
THRESHOLD = 0.15


def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_highpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def apply_filter(data):
    b, a = butter_lowpass(cutoff_low, fs, order=order)
    #y = lfilter(b, a, data)
    y = signal.filtfilt(b, a, data)

    b, a = butter_highpass(cutoff_high, fs, order)
    y_ = signal.filtfilt(b, a, y)
    return y_

# Step 1 and 2
# This method removes offset from time domain data
# @params filename
# @returns dataframe


def get_time_domain_without_offset(filename):
    data_frame = pd.read_csv(filename, skiprows=[0], header=None)
    required_data_frame = data_frame.iloc[:, DATA_HEADERS_SIZE:]
    return required_data_frame.sub(required_data_frame.mean(axis=1), axis=0)

# Step 3
# this method applies low and high pass filter to time domain data
# @params data_frame
# @returns list


def get_filtered_values(data_frame):
    new_data = []
    for data in data_frame.values:
        new_data.append(apply_filter(data))
    new_data = np.array(new_data)
    return new_data

# Step 4:


def peak_value(data):
    max_point_distance = 0
    peakData = 0
    max_point_distance = np.array(data).argmax()
    peakData = np.array(data).max()
    if peakData > THRESHOLD:
        return max_point_distance
    else:
        return None


def get_echos(filtered_values):
    all_echo_range = []
    cut_index_list = []
    chopped_data = filtered_values[:, NOISE_SIZE:]
    for index, data in enumerate(chopped_data):
        max_point_distance = peak_value(data)
        if max_point_distance:
            cutting_distance = max_point_distance - ECHO_SIZE_LEFT
            if cutting_distance > 0:
                echo_range = data[cutting_distance:]
                echo_range = echo_range[:ECHO_SIZE_RIGHT]
                all_echo_range.append(echo_range)
            else:
                cut_index_list.append(index)
    return all_echo_range


def save_to_csv(echo_set, folder, file):
    df = pd.DataFrame(echo_set)
    df.to_csv('./Documents/data_set/Result/{}/{}_overall.csv'.format(folder,
                                                                     file), header=False, index=False)


def get_echos_from_file(file_name):
    time_domain_data_without_offset = get_time_domain_without_offset(file_name)
    filtered_values = get_filtered_values(time_domain_data_without_offset)
    echos_data = get_echos(filtered_values)
    return echos_data


if __name__ == '__main__':
    print('data_processing')
