import sys

import rtmidi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QHBoxLayout

midiout = rtmidi.MidiOut()


class ScanMidiDevices(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Hello, world!'
        # self.left = 10
        # self.top = 10
        # self.width = 640
        # self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        layout = QHBoxLayout()

        self.cb = QComboBox()
        self.cb.addItems(midiout.get_ports())
        layout.addWidget(self.cb)

        self.button = QPushButton('Reload', self)
        self.button.setToolTip('Reload visible midi controller')
        layout.addWidget(self.button)

        self.button = QPushButton('Connect', self)
        self.button.setToolTip('Connect to selected midi device')
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScanMidiDevices()
    sys.exit(app.exec_())
