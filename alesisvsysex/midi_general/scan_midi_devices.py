import sys

import rtmidi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QHBoxLayout
from alesisvsysex.device.alesis import AlesisV25Device

from alesisvsysex.ui.window import AlesisVSysexApplication


class ScanMidiDevices(QWidget):
    def __init__(self):
        super().__init__()
        self.midiout = rtmidi.MidiOut()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Midi Scan')
        layout = QHBoxLayout()

        self.cb = QComboBox()
        self.cb.addItems(self.midiout.get_ports())
        layout.addWidget(self.cb)

        self.button_reload = QPushButton('Reload', self)
        self.button_reload.setToolTip('Reload visible midi controller')
        self.button_reload.clicked.connect(self.click_reload)
        layout.addWidget(self.button_reload)

        self.button_connect = QPushButton('Connect', self)
        self.button_connect.setToolTip('Connect to selected midi device')
        self.button_connect.clicked.connect(self.click_connect)
        layout.addWidget(self.button_connect)

        self.setLayout(layout)
        self.show()

    def click_reload(self):
        self.cb.clear()
        self.cb.addItems(self.midiout.get_ports())

    def click_connect(self):
        selected_midi_controller = self.cb.currentText()
        AlesisV25Device._PORT_PREFIX = selected_midi_controller

        alesis_app = AlesisVSysexApplication()
        alesis_app.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScanMidiDevices()
    sys.exit(app.exec_())
