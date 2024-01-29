from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """ Signal bus """

    modelChanged = Signal()
    micaEnableChanged = Signal(bool)


signalBus = SignalBus()