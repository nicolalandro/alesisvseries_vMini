import rtmidi
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QSpinBox, QGroupBox, \
    QFormLayout, QLabel, QVBoxLayout, QProgressBar

from midi_knobs_gui.knob_worker import SimulRunner


class KnobGui(QWidget):
    def __init__(self):
        super().__init__()
        self.midiout = rtmidi.MidiOut()
        self.port = None
        self.initUI()

        # create
        self.simulRunner = SimulRunner()
        self.simulThread = QThread()
        self.simulRunner.moveToThread(self.simulThread)

        # start and listen
        self.simulThread.start()
        self.simulThread.started.connect(self.simulRunner.longRunning)
        self.simulRunner.stepIncreased.connect(self.knob_update)

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
