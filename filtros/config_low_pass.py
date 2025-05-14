from scipy.signal import butter, tf2sos, cheby2
import numpy as np
import matplotlib.pyplot as plt

def lowPassConfig(fc, N = 8, fs = 44100):
    wn = fc / (fs / 2)
    b, a = butter(N, wn, btype='low', analog=False, output='ba')
    return b, a, N

# def lowPassConfig(fc, N = 10, fs = 88200, Astop = 80):
#     wn = fc / (fs / 2)
#     b, a = cheby2(N, Astop, fc, btype='low', fs=fs)
#     return b, a, N
