import time

import mido
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication


class SimulRunner(QObject):
    'Object managing the simulation'

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
                if r.type == 'control_change' and r.channel == 0 and r.control == 14:
                    print(r.value)
                    self.stepIncreased.emit(r.value)
                # time.sleep(0.1)

    def start(self):
        self.midi_device = mido.open_ioport('VMini:VMini MIDI 1 20:0')
        self._isRunning = True

    def stop(self):
        self._isRunning = False
        self.midi_device.close()
