def get_echo_peaks(peaks, window_size=1024, echo_left_size=256):
    prev_value = peaks[0]
    echos = []
    for i in peaks:
        if len(echos):
            if i - prev_value > 1024:
                echos.append(i)
        if not len(echos) and i > echo_left_size:
            echos = [i]
        prev_value = i
    return echos
