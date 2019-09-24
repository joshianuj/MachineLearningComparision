import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

from scipy.signal import butter, lfilter, freqz
from scipy import signal
data_after_applying_filter = []

cutoff = 3000 #in Hz
fs = 114*1000 # 5micro samples per second
order = 5
NOISE_SIZE = 350
ECHO_SIZE = 200
THRESHOLD = 0.15

def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    #y = lfilter(b, a, data)
    y = signal.filtfilt(b, a, data)
    return y

#Step 1 and 2
def get_time_domain_without_offset(filename):
    data_frame = pd.read_csv(filename, skiprows=[0], header= None)
    required_data_frame = data_frame.iloc[:, 9:]
    required_data_without_offset = required_data_frame.sub(required_data_frame.mean(axis=1), axis=0).values
    return required_data_without_offset

#Step 3
def use_low_pass_filter(data_values):
    data_after_applying_filter = []
    for i, data in enumerate(data_values):
        y = butter_lowpass_filter(data, cutoff, fs, order)
        result = data - y
        data_after_applying_filter.append(result)
    return data_after_applying_filter

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
    for index, data in enumerate(filtered_values):
        chopped_data = data[NOISE_SIZE:]
        max_point_distance = peak_value(chopped_data)
        if max_point_distance:
            cutting_distance = max_point_distance - 100
            if cutting_distance > 0:
                echo_range = chopped_data[cutting_distance:]
                echo_range = echo_range[:ECHO_SIZE]
                all_echo_range.append(echo_range)
    return all_echo_range

def save_to_csv(echo_set, folder, file):
    df = pd.DataFrame(echo_set)
    print(folder,file)
    df.to_csv('./Documents/data_set/Result/{}/{}_overall.csv'.format(folder, file), header=False, index=False)

if __name__ == '__main__':
    print('data_processing')