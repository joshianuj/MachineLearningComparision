def get_echo_peaks(peaks, window_size=1024, echo_left_size=256):
    prev_value = peaks[0]
    echos = []
    if peaks[0] > echo_left_size:
        echos.append(peaks[0])
    for i in peaks:
        if len(echos):
            if i - prev_value - echo_left_size > window_size:
                prev_value = i
                echos.append(i)
    return echos
