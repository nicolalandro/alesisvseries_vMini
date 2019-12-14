#! /usr/bin/python

import os
import sys

try:
    import mido
except:
    print('Python3 lib "mido" is not installed, try to exec "pip install mido"')
    exit(1)
try:
    import rtmidi
except:
    print('Python3 lib "python-rtmidi" is not installed, try to exec "pip install python-rtmidi"')
    exit(1)

try:
    from PyQt5.QtCore import QObject, pyqtSignal
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QThread
    from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QSpinBox, QGroupBox, \
        QFormLayout, QLabel, QVBoxLayout, QProgressBar
except:
    print('PyQt5 is not installed, try to install it')
    exit(1)


class SimulRunner(QObject):
    stepIncreased = pyqtSignal(int, name='stepIncreased')

    def __init__(self):
        super(SimulRunner, self).__init__()
        self._step = 0
        self._isRunning = False
        self._maxSteps = 20

    def longRunning(self):
        while True:
            QApplication.processEvents()
            if self._isRunning == True:
                r = self.midi_device.receive()
                if r.type == 'control_change' and r.channel == self.channel and r.control == self.control:
                    self.stepIncreased.emit(r.value)
                    os.system(('pactl set-sink-volume 0 %d' % r.value) + '%')

    def start(self, name, channel, control):
        self.midi_device = mido.open_ioport(name)
        self.channel = channel
        self.control = control
        self._isRunning = True

    def stop(self):
        self._isRunning = False
        self.midi_device.close()


class KnobGui(QWidget):
    def __init__(self):
        super().__init__()
        self.midiout = rtmidi.MidiOut()
        self.port = None
        self.init_ui()
        self.init_background_thread()

    def init_background_thread(self):
        # create
        self.simulRunner = SimulRunner()
        self.simulThread = QThread()
        self.simulRunner.moveToThread(self.simulThread)
        # start and listen
        self.simulThread.start()
        self.simulThread.started.connect(self.simulRunner.longRunning)
        self.simulRunner.stepIncreased.connect(self.knob_update)

    def init_ui(self):
        self.setWindowTitle('Midi Knobs to Master Audio Volume')
        layout = QVBoxLayout()

        connect_form = self.create_connect_form()
        layout.addWidget(connect_form)

        knob_form = self.create_knob_form()
        layout.addWidget(knob_form)

        self.setLayout(layout)
        self.show()

    def create_connect_form(self):
        form_group = QGroupBox("Midi Controller")
        layout = QFormLayout()
        self.cb = QComboBox()
        self.cb.addItems(self.midiout.get_ports())
        layout.addRow(QLabel("Select Device:"), self.cb)

        self.button_connect = QPushButton('Connect', self)
        self.button_connect.setToolTip('Connect to selected midi device')
        self.button_connect.clicked.connect(self.click_connect)

        self.button_disconnect = QPushButton('Disconnect', self)
        self.button_disconnect.setToolTip('Disconnect to midi controller')
        self.button_disconnect.clicked.connect(self.click_disconnect)

        layout.addRow(self.button_connect, self.button_disconnect)

        form_group.setLayout(layout)
        return form_group

    def create_knob_form(self):
        form_group = QGroupBox("Knob")
        layout = QFormLayout()

        self.channel = QSpinBox()
        self.channel.setToolTip('Midi knob channel')
        layout.addRow(QLabel("Channel:"), self.channel)

        self.control = QSpinBox()
        self.control.setToolTip('Midi knob control')
        self.control.setValue(14)
        layout.addRow(QLabel("Control:"), self.control)

        self.progress_bar = QProgressBar()
        self.progress_bar.setToolTip('Value')
        self.progress_bar.setRange(0, 127)
        layout.addRow(self.progress_bar)

        form_group.setLayout(layout)
        return form_group

    def click_disconnect(self):
        self.simulRunner.stop()
        self.close()

    def click_connect(self):
        selected_midi_controller = self.cb.currentText()
        channel = int(self.channel.value())
        control = int(self.control.value())
        self.simulRunner.start(selected_midi_controller, channel, control)

    def knob_update(self, value):
        self.progress_bar.setValue(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KnobGui()
    sys.exit(app.exec_())
