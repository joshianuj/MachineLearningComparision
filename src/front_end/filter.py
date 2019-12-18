import pandas as pd
import numpy as np

from scipy.signal import butter, lfilter, freqz
from scipy import signal

from utils.peaks_util import get_echo_peaks

SAMPLE_FREQUENCY_COMBO_BOX = {
    '2.86MHz': {
        'value': 2.86*1e6,
        'echo_size': 4096,
        'noise_size': 0,
        'threshold': 0.15,
        'variance_threshold': 0.02,
        'echo': './data/echo/2MHz/',
        'features': './data/features/2MHz/',
    }, '1.14MHz': {
        'value': 1.14*1e6,
        'echo_size': 2048,
        'noise_size': 0,
        'threshold': 0.15,
        'variance_threshold': 0.02,
        'echo': './data/echo/1MHz/',
        'features': './data/features/1MHz/',
    },
    '114KHz': {
        'value': 114*1e6,
        'echo_size': 1024,
        'noise_size': 350,
        'threshold': 0.15,
        'variance_threshold': 0.02,
        'echo': './data/echo/114KHz/',
        'features': './data/features/114KHz/',
    }
}


class DataProcessor:
    def __init__(self):
        self.selected_element = SAMPLE_FREQUENCY_COMBO_BOX['2.86MHz']
        self.LOW_PASS = 60*1e3
        self.HIGH_PASS = 30*1e3
        self.NOISE_SIZE = SAMPLE_FREQUENCY_COMBO_BOX['2.86MHz']['noise_size']
        self.THRESHOLD = 0.15
        self.DATA_HEADERS_SIZE = 9
        self.ECHO_SIZE_LEFT = 300
        self.ECHO_SIZE = SAMPLE_FREQUENCY_COMBO_BOX['2.86MHz']['echo_size']
        self.order = 5
        self.VARIANCE_THRESHOLD = SAMPLE_FREQUENCY_COMBO_BOX['2.86MHz']['variance_threshold']

    def change_selected_element(self, element_name):
        if element_name in SAMPLE_FREQUENCY_COMBO_BOX:
            self.selected_element = SAMPLE_FREQUENCY_COMBO_BOX[element_name]
            self.ECHO_SIZE = SAMPLE_FREQUENCY_COMBO_BOX[element_name]['echo_size']
            self.NOISE_SIZE = SAMPLE_FREQUENCY_COMBO_BOX[element_name]['noise_size']
            self.THRESHOLD = SAMPLE_FREQUENCY_COMBO_BOX[element_name]['threshold']
            self.VARIANCE_THRESHOLD = SAMPLE_FREQUENCY_COMBO_BOX[element_name]['variance_threshold']

    def butter_lowpass(self, cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_highpass(self, cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def apply_filter(self, data):
        b, a = self.butter_lowpass(
            self.LOW_PASS, self.selected_element['value'], order=self.order)
        # y = lfilter(b, a, data)
        y = signal.filtfilt(b, a, data)

        b, a = self.butter_highpass(
            self.HIGH_PASS, self.selected_element['value'], self.order)
        y_ = signal.filtfilt(b, a, y)
        return y_

    # Step 1 and 2
    # This method removes offset from time domain data
    # @params filename
    # @returns dataframe

    def get_time_domain_without_offset(self, filename):
        data_frame = pd.read_csv(filename, skiprows=[0], header=None)
        required_data_frame = data_frame.iloc[:, self.DATA_HEADERS_SIZE:]
        return required_data_frame.sub(required_data_frame.mean(axis=1), axis=0)

    # Step 3
    # this method applies low and high pass filter to time domain data
    # @params data_frame
    # @returns list

    def get_filtered_values(self, data_frame):
        new_data = []
        for data in data_frame.values:
            new_data.append(self.apply_filter(data))
        new_data = np.array(new_data)
        return new_data

    def peak_value(self, data):
        max_point_distance = 0
        peakData = 0
        max_point_distance = np.array(data).argmax()
        peakData = np.array(data).max()
        if peakData > self.THRESHOLD:
            return max_point_distance
        else:
            return None

    def get_echos(self, filtered_values):
        all_echo_range = []
        cut_index_list = []
        chopped_data = filtered_values[:, self.NOISE_SIZE:]
        for index, data in enumerate(chopped_data):
            max_point_distance = self.peak_value(data)
            if max_point_distance:
                cutting_distance = max_point_distance - self.ECHO_SIZE_LEFT
                if cutting_distance > 0:
                    echo_range = data[cutting_distance:]
                    echo_range = echo_range[:self.ECHO_SIZE]
                    all_echo_range.append(echo_range)
                else:
                    cut_index_list.append(index)
        return all_echo_range

    def get_echo_set_location(self, data):
        data = np.array(data)
        no_of_windows = round(data.size[1]/self.ECHO_SIZE)
        echo_set = []
        for d in data:
            window_peak_locations = []
            for i in range(0, no_of_windows):
                window_peak = d[i*self.ECHO_SIZE:(i+1)*self.ECHO_SIZE].max()
                if window_peak >= self.THRESHOLD:
                    window_peak_location = i*self.ECHO_SIZE + \
                        d[i*self.ECHO_SIZE:(i+1)*self.ECHO_SIZE].argmax()
                    if i > 0 or window_peak_location > self.ECHO_SIZE_LEFT:
                        window_peak_locations.append(window_peak_location)
            echos = []
            if len(window_peak_locations):
                echos = [window_peak_locations[0]]
                prev_echo = window_peak_locations[0]
                for w in window_peak_locations:
                    if prev_echo - w > self.ECHO_SIZE:
                        echos.append(w)
                    prev_echo = w
            echo_set.append(echos)
        return echo_set

    def find_echos(self, data_values):
        # data_values = data_values[:, self.NOISE_SIZE:]
        dfObj = pd.DataFrame(data_values)
        rolling_variance_dataframe = dfObj.rolling(
            window=100, axis=1).var()
        echo_list = []
        for i, d in enumerate(rolling_variance_dataframe.values):
            peaks, _ = signal.find_peaks(d, height=self.VARIANCE_THRESHOLD)
            if len(peaks):
                echo_peaks = get_echo_peaks(
                    peaks, self.ECHO_SIZE, self.ECHO_SIZE_LEFT)
                if len(echo_peaks):
                    for index, e in enumerate(echo_peaks):
                        echo_left_size = e - self.ECHO_SIZE_LEFT
                        echo_data = {
                            'ECHO': data_values[i][slice(echo_left_size, echo_left_size+self.ECHO_SIZE)],
                            'ECHO_COUNTER': index + 1
                        }
                        echo_list.append(echo_data)
        if len(echo_list):
            df = pd.DataFrame.from_dict(echo_list)
            df_with_echo = pd.concat(
                [df.ECHO_COUNTER, pd.DataFrame(df.ECHO.tolist())], axis=1)
            return df_with_echo
        return None
