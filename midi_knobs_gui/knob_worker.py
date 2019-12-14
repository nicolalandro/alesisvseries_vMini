import time

from PyQt5.QtCore import QObject, pyqtSignal


class SimulRunner(QObject):
    'Object managing the simulation'

    stepIncreased = pyqtSignal(int, name='stepIncreased')

    def __init__(self):
        super(SimulRunner, self).__init__()
        self._step = 0
        self._isRunning = True
        self._maxSteps = 20

    def longRunning(self):
        while self._isRunning == True:
            self._step += 1
            self.stepIncreased.emit(self._step)
            time.sleep(0.1)

    def stop(self):
        self._isRunning = False
