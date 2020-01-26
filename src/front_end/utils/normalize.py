import numpy as np

def custom_normalization(X_set):
    new_X_set = []
    for X in X_set:
        min = np.min(X)
        max = np.max(X)
        value = max - min
        data_set = []
        for data in X:
            data_set.append(((data - min) / value) + 0)
        new_X_set.append(data_set)
    return new_X_set