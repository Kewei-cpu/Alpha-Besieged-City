from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QWidget
from qfluentwidgets import CardWidget, CaptionLabel, FlowLayout, isDarkTheme, SingleDirectionScrollArea, setFont
from app.common import convertMoveToNotation


class SingleStepCard(CardWidget):
    """ Emoji card """

    def __init__(self, text, index, func, parent=None):
        self.index = index
        self.color = QColor(60, 144, 217) if index % 2 == 0 else QColor(26, 177, 100)
        self.active = False

        super().__init__(parent)

        self.label = CaptionLabel(text, self)
        setFont(self.label, 16)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.label)

        self.setFixedSize(100, 35)

        self.clicked.connect(lambda: func(index))

    def setActive(self, active):
        self.active = active
        self._updateBackgroundColor()


    def _normalBackgroundColor(self):
        c = self.color.__copy__()
        if self.active:
            c.setAlpha(40 if isDarkTheme() else 80)
        else:
            c.setAlpha(13 if isDarkTheme() else 32)
        return c

    def _hoverBackgroundColor(self):
        c = self.color.__copy__()
        c.setAlpha(21 if isDarkTheme() else 16)
        return self.color

    def _pressedBackgroundColor(self):
        c = self.color.__copy__()
        c.setAlpha(21 if isDarkTheme() else 16)
        return self.color


class StepScrollArea(SingleDirectionScrollArea):
    def __init__(self):
        super().__init__()

        self.view = QWidget(self)
        self.view.setFixedWidth(230)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setMinimumWidth(230)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')

        self.flowLayout = FlowLayout(self.view)

        self.flowLayout.setSpacing(5)
        self.flowLayout.setContentsMargins(10, 10, 10, 10)
        self.flowLayout.setAlignment(Qt.AlignVCenter)


class StepCard(CardWidget):
    def __init__(self, func):
        super().__init__()
        self.scroll_area = StepScrollArea()
        self.func = func

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.scroll_area)

    def addSteps(self, history):
        for i in reversed(range(self.scroll_area.flowLayout.count())):
            self.scroll_area.flowLayout.itemAt(i).widget().setParent(None)

        notations = convertMoveToNotation(history)

        for i, note in enumerate(notations):
            self.scroll_area.flowLayout.addWidget(SingleStepCard(note, i, self.func))

    def setActiveStep(self, index):
        for i in range(self.scroll_area.flowLayout.count()):
            self.scroll_area.flowLayout.itemAt(i).widget().setActive(False)
        self.scroll_area.flowLayout.itemAt(index).widget().setActive(True)