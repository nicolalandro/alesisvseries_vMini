import sys

from PyQt5.QtWidgets import QApplication

from midi_knobs_gui.knobs_gui import KnobGui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KnobGui()
    sys.exit(app.exec_())
