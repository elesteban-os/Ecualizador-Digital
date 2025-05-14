import numpy as np
#from pyqtgraph.Qt import QtCore, QtWidgets


import pyqtgraph as pg

import pyaudio
from scipy.fftpack import fft

from filter_data import getFilterData
from iir_filter import iir_filter

from filtros.config_low_pass import lowPassConfig

import sys
from PyQt5 import QtCore as QtCore, QtWidgets

class AudioStream(object):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        # pyqtgraph stuff
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Spectrum Analyzer')
        self.win.setGeometry(5, 115, 1910, 1070)
        self.win.show()

        # Crear un contenedor para los botones y el slider
        self.container = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()

        # Agregar checkboxes
        self.checkboxes = []
        
        # Low pass
        checkbox_lp = QtWidgets.QCheckBox("Low Pass")
        checkbox_lp.stateChanged.connect(lambda state: self.on_checkbox_change_lp(0, state))
        self.layout.addWidget(checkbox_lp)
        self.checkboxes.append(checkbox_lp)

        # High pass
        checkbox_hp = QtWidgets.QCheckBox("High Pass")
        checkbox_hp.stateChanged.connect(lambda state: self.on_checkbox_change_hp(1, state))
        self.layout.addWidget(checkbox_hp)
        self.checkboxes.append(checkbox_hp)

        # Band pass
        checkbox_bp = QtWidgets.QCheckBox("Band Pass")
        checkbox_bp.stateChanged.connect(lambda state: self.on_checkbox_change_bp(2, state))
        self.layout.addWidget(checkbox_bp)
        self.checkboxes.append(checkbox_bp)

        # Band stop
        checkbox_sp = QtWidgets.QCheckBox("Band Stop")
        checkbox_sp.stateChanged.connect(lambda state: self.on_checkbox_change_sp(3, state))
        self.layout.addWidget(checkbox_sp)
        self.checkboxes.append(checkbox_sp)

        # Custom Low Pass
        checkbox_clp = QtWidgets.QCheckBox("Adjustable Low Pass")
        checkbox_clp.stateChanged.connect(lambda state: self.on_checkbox_change_clp(4, state))
        self.layout.addWidget(checkbox_clp)
        self.checkboxes.append(checkbox_clp)

        # Agregar slider
        self.slider = QtWidgets.QSlider()
        self.slider = QtWidgets.QSlider(orientation=QtCore.Qt.Horizontal)
        self.slider.setMinimum(500)
        self.slider.setMaximum(15000)
        self.slider.setValue(1000)
        
        self.slider.setMinimumWidth(300)  # O prueba con setFixedWidth(400)
        self.slider.valueChanged.connect(self.on_slider_change)
        self.layout.addWidget(self.slider)

        # Crea la etiqueta que mostrará el valor del slider
        self.slider_label = QtWidgets.QLabel("Frequency: " + str(self.slider.value()))

        # Agrega el slider y la etiqueta al layout horizontal
        self.layout.addWidget(self.slider_label)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.slider_label)

        # Finalmente, agrega este layout al layout principal de la ventana
        self.layout.addLayout(self.layout)

        # Configurar el diseño del contenedor
        self.container.setLayout(self.layout)
        self.container.setGeometry(10, 10, 200, 300)
        self.container.show()

        # Mostrar la ventana principal
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

        self.lpcfilter_data = lowPassConfig(1000)
        self.lpcfilter = iir_filter(b=self.lpcfilter_data[0], a=self.lpcfilter_data[1])

        self.lpActive = False
        self.hpActive = False
        self.bpActive = False
        self.spActive = False
        self.clpActive = False
        self.clowpassValue = 1000

        # Checkboxes
    def on_checkbox_change_lp(self, checkbox_index, state):
        self.lpActive = not self.lpActive

    def on_checkbox_change_hp(self, checkbox_index, state):
        self.hpActive = not self.hpActive

    def on_checkbox_change_bp(self, checkbox_index, state):
        self.bpActive = not self.bpActive

    def on_checkbox_change_sp(self, checkbox_index, state):
        self.spActive = not self.spActive

    def on_checkbox_change_clp(self, checkbox_index, state):
        self.clpActive = not self.clpActive

    def on_slider_change(self, value):
        #print(f"Slider value: {value}")
        self.lpcfilter_data = lowPassConfig(self.clowpassValue)
        self.slider_label.setText("Frequency: " + str(value))
        self.clowpassValue = value

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec()

    def on_button_click(self, button_index):
        print(f"Button {button_index + 1} clicked!")

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
        
        # Apply filters based on active variables
        if self.lpActive:
            wf_data = self.lpfilter.filter(wf_data)
        if self.hpActive:
            wf_data = self.hpfilter.filter(wf_data)
        if self.bpActive:
            wf_data = self.bpfilter.filter(wf_data)
        if self.spActive:
            wf_data = self.sbfilter.filter(wf_data)
        if self.clpActive:
            self.lpcfilter = iir_filter(b=self.lpcfilter_data[0], a=self.lpcfilter_data[1])
            wf_data = self.lpcfilter.filter(wf_data)

        # Plot data
        self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)

        sp_data = fft(np.array(wf_data, dtype='int16') - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]
                         ) * 2 / (128 * self.CHUNK)
        self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
        
        # Write data
        self.stream.write(wf_data.astype(np.int16).tobytes(), self.CHUNK)

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)
        self.start()



if __name__ == '__main__':

    audio_app = AudioStream()
    audio_app.animation()
