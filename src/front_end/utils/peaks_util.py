def find_echo_from_peaks(peaks, window_size=1024):
    echos = []
    if len(peaks):
        prev_value = peaks[0]
        echos = [peaks[0]]
        for i in peaks:
            if i - prev_value > window_size:
                echos.append(i)
            prev_value = i
    echos
