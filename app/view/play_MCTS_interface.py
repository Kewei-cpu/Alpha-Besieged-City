from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import PushButton, ComboBox, FluentIcon

from app.widgets.board_widget import BoardWidget


class PlayMCTSInterface(QWidget):
    def __init__(self, text, parent):
        super().__init__(parent)
        self.setMinimumSize(600, 500)
        self.setMouseTracking(True)
        self.setObjectName(text.replace(' ', '-'))

        self.board_widget = BoardWidget(text, self)
        self.board_widget.onEnableNN()

        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.restart_button = PushButton(self)
        self.restart_button.setText("New")
        self.restart_button.setIcon(FluentIcon.ADD)
        self.restart_button.clicked.connect(self.board_widget.onRestart)
        self.button_layout.addWidget(self.restart_button)

        self.load_button = PushButton(self)
        self.load_button.setText("Import")
        self.load_button.setIcon(FluentIcon.DOWNLOAD)
        self.load_button.clicked.connect(self.board_widget.onLoad)
        self.button_layout.addWidget(self.load_button)

        self.first_button = PushButton(self)
        self.first_button.setText("First")
        self.first_button.setIcon(FluentIcon.LEFT_ARROW)
        self.first_button.clicked.connect(self.board_widget.onFirst)
        self.board_widget.onNotFirstMove.connect(self.first_button.setEnabled)
        self.button_layout.addWidget(self.first_button)

        self.previous_button = PushButton(self)
        self.previous_button.setText("Previous")
        self.previous_button.setIcon(FluentIcon.PAGE_LEFT)
        self.previous_button.clicked.connect(self.board_widget.onPrevious)
        self.board_widget.onNotFirstMove.connect(self.previous_button.setEnabled)
        self.button_layout.addWidget(self.previous_button)

        self.next_button = PushButton(self)
        self.next_button.setText("Next")
        self.next_button.setIcon(FluentIcon.PAGE_RIGHT)
        self.next_button.clicked.connect(self.board_widget.onNext)
        self.board_widget.onNotLastMove.connect(self.next_button.setEnabled)
        self.button_layout.addWidget(self.next_button)

        self.last_button = PushButton(self)
        self.last_button.setText("Last")
        self.last_button.setIcon(FluentIcon.RIGHT_ARROW)
        self.last_button.clicked.connect(self.board_widget.onLast)
        self.board_widget.onNotLastMove.connect(self.last_button.setEnabled)
        self.button_layout.addWidget(self.last_button)

        self.skip_button = PushButton(self)
        self.skip_button.setText("Skip")
        self.skip_button.setIcon(FluentIcon.CHEVRON_RIGHT)
        self.skip_button.clicked.connect(self.board_widget.nnMove)
        self.board_widget.onSkipAvailable.connect(self.skip_button.setEnabled)
        self.button_layout.addWidget(self.skip_button)

        self.save_button = PushButton(self)
        self.save_button.setText("Save")
        self.save_button.setIcon(FluentIcon.SAVE)
        self.save_button.clicked.connect(self.board_widget.onSave)
        self.board_widget.onSaveAvailable.connect(self.save_button.setEnabled)
        self.button_layout.addWidget(self.save_button)


        self.main_layout.addWidget(self.board_widget)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
