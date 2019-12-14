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
                print('if')
                r = self.midi_device.receive()
                if r.type == 'control_change' and r.channel == self.channel and r.control == self.control:
                    print(r.value)
                    self.stepIncreased.emit(r.value)
                # time.sleep(0.1)
            else:
                print('else')

    def start(self, name, channel, control):
        self.midi_device = mido.open_ioport(name)
        self.channel = channel
        self.control = control
        self._isRunning = True

    def stop(self):
        self._isRunning = False
        self.midi_device.close()
