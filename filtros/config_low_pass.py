from scipy.signal import butter, tf2sos
import numpy as np
import matplotlib.pyplot as plt

def lowPassConfig(fc, N = 8, fs = 44100):
    wn = fc / (fs / 2)
    b, a = butter(N, wn, btype='low', analog=False, output='ba')
    return b, a, N


while True:
    freq = input("Frecuencia de corte [Hz]: ")
    freqnum = int(freq)
    a, b, N = lowPassConfig(freqnum)
    print(a)
    print(b)
    print(N)