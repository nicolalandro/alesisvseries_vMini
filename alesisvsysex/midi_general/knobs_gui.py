import os
import sys
from asyncio import async

import mido
import rtmidi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QSpinBox, QGroupBox, \
    QFormLayout, QLabel, QVBoxLayout, QProgressBar


class KnobGui(QWidget):
    def __init__(self):
        super().__init__()
        self.midiout = rtmidi.MidiOut()
        self.port = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Midi Scan')
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

        channel = QSpinBox()
        channel.setToolTip('Midi knob channel')
        layout.addRow(QLabel("Channel:"), channel)

        control = QSpinBox()
        control.setToolTip('Midi knob control')
        layout.addRow(QLabel("Control:"), control)

        self.progress_bar = QProgressBar()
        self.progress_bar.setToolTip('Value')
        self.progress_bar.setRange(0, 127)
        layout.addRow(self.progress_bar)

        form_group.setLayout(layout)
        return form_group

    def click_disconnect(self):
        self.port.close()

    def click_connect(self):
        selected_midi_controller = self.cb.currentText()
        self.port = mido.open_ioport(selected_midi_controller)

    def knob_update(self, value):
        self.progress_bar.setValue(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KnobGui()
    sys.exit(app.exec_())
