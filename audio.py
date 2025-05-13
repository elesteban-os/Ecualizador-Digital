import numpy as np
from pyqtgraph.Qt import QtCore, QtWidgets
import pyqtgraph as pg

import pyaudio
from scipy.fftpack import fft

from filter_data import getFilterData
from iir_filter import iir_filter

import sys


class AudioStream(object):
    def __init__(self):

        # pyqtgraph stuff
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Spectrum Analyzer')
        self.win.setGeometry(5, 115, 1910, 1070)
        self.win.show()

        wf_xlabels = [(0, '0'), (1024, '1024'), (2048, '2048')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [
            (-32768, '-32768'),
            (-16384, '-16384'),
            (0, '0'),
            (16384, '16384'),
            (32767, '32767')
        ]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        sp_xlabels = [
            (np.log10(10), '10'), (np.log10(100), '100'),
            (np.log10(1000), '1000'), (np.log10(10000), '10000'), (np.log10(22050), '22050')
        ]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])

        self.waveform = self.win.addPlot(
            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
        )
        self.spectrum = self.win.addPlot(
            title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis},
        )

        # pyaudio stuff
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        # waveform and spectrum x points
        self.x = np.arange(0, self.CHUNK)
        self.f = np.linspace(0, self.RATE / 2, int(self.CHUNK / 2))

        # filter stuff
        self.lpfilter_path = 'filtros/pasa_bajas.fcf'
        self.lpfilter_data = getFilterData(self.lpfilter_path)
        self.lpfilter = iir_filter(b=self.lpfilter_data[0], a=self.lpfilter_data[1])

        self.hpfilter_path = 'filtros/pasa_altas.fcf'
        self.hpfilter_data = getFilterData(self.hpfilter_path)
        self.hpfilter = iir_filter(b=self.hpfilter_data[0], a=self.hpfilter_data[1])

        self.bpfilter_path = 'filtros/pasa_bandas.fcf'
        self.bpfilter_data = getFilterData(self.bpfilter_path)
        self.bpfilter = iir_filter(b=self.bpfilter_data[0], a=self.bpfilter_data[1])

        self.sbfilter_path = 'filtros/suprime_bandas.fcf'
        self.sbfilter_data = getFilterData(self.sbfilter_path)
        self.sbfilter = iir_filter(b=self.sbfilter_data[0], a=self.sbfilter_data[1])

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(-32767, 32767, padding=0)
                self.waveform.setXRange(0, self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 2, padding=0)
                self.spectrum.setXRange(
                    np.log10(20), np.log10(self.RATE / 2), padding=0.005)

    def update(self):
        # Read data
        wf_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        wf_data = np.frombuffer(wf_data, dtype=np.int16)
        
        # Apply filter
        wf_data = self.sbfilter.filter(wf_data)

        # Plot data
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)

        sp_data = fft(np.array(wf_data, dtype='int16') - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]
                         ) * 2 / (128 * self.CHUNK)
        self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
        
        # Write data
        #self.stream.write(wf_data, self.CHUNK)

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()



if __name__ == '__main__':

    audio_app = AudioStream()
    audio_app.animation()
