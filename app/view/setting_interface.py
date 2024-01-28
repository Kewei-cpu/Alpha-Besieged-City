# coding: utf-8

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, RangeSettingCard, PushSettingCard,
                            ColorSettingCard, ScrollArea,
                            ExpandLayout, Theme, InfoBar, setTheme, FluentIcon, TitleLabel)

from app.config import *




class SettingInterface(ScrollArea):
    enableAcrylicChanged = Signal(bool)
    MCTSRefreshSignal = Signal()

    def __init__(self, text, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(text.replace(' ', '-'))

        self.scrollWidget = QWidget(self)

        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.settingsLabel = TitleLabel('Settings', self.scrollWidget)
        self.settingsLabel.setFixedHeight(40)

        self.AppearanceGroup = SettingCardGroup("Appearance", self.scrollWidget)

        self.themeModeCard = OptionsSettingCard(
            cfg.themeMode,
            FluentIcon.BRUSH,
            "Application Theme",
            "Change the appearance of your application",
            texts=['Light', 'Dark', 'Use system setting'],
            parent=self.AppearanceGroup,
        )
        self.themeColorCard = ColorSettingCard(
            cfg.themeColor,
            FluentIcon.PALETTE,
            "Theme Color",
            "Change the theme color of you application",
            parent=self.AppearanceGroup,
        )
        self.boardBackgroundColorCard = OptionsSettingCard(
            cfg.boardBackground,
            FluentIcon.PALETTE,
            "Board Background Color",
            "Change the background of the board",
            texts=BoardBackgroundColorEnum.values(),
            parent=self.AppearanceGroup,
        )
        self.boardBackgroundAlphaCard = RangeSettingCard(
            cfg.boardBackgroundAlpha,
            FluentIcon.SETTING,
            "Board Background Opacity",
            "Change the opacity of the board background",
            parent=self.AppearanceGroup
        )
        self.boardGridColorCard = OptionsSettingCard(
            cfg.boardGridColor,
            FluentIcon.PALETTE,
            "Board Grid Color",
            "Change the grid color of the board",
            texts=BoardGridColorEnum.values(),
            parent=self.AppearanceGroup,
        )
        self.boardGridAlphaCard = RangeSettingCard(
            cfg.boardGridAlpha,
            FluentIcon.SETTING,
            "Board Grid Opacity",
            "Change the opacity of the board gird",
            parent=self.AppearanceGroup
        )

        self.AppearanceGroup.addSettingCard(self.themeModeCard)
        self.AppearanceGroup.addSettingCard(self.themeColorCard)
        self.AppearanceGroup.addSettingCard(self.boardBackgroundColorCard)
        self.AppearanceGroup.addSettingCard(self.boardBackgroundAlphaCard)
        self.AppearanceGroup.addSettingCard(self.boardGridColorCard)
        self.AppearanceGroup.addSettingCard(self.boardGridAlphaCard)

        self.musicInThisPCGroup = SettingCardGroup("Alpha Besieged City on this PC", self.scrollWidget)

        self.modelFolderCard = PushSettingCard(
            "Choose Folder",
            FluentIcon.FOLDER,
            "Model directory",
            cfg.get(cfg.modelPath),
            parent=self.musicInThisPCGroup
        )

        self.musicInThisPCGroup.addSettingCard(self.modelFolderCard)

        self.MCTSGroup = SettingCardGroup("MCTS", self.scrollWidget)

        self.cPuctCard = RangeSettingCard(
            cfg.cPuct,
            FluentIcon.SETTING,
            "Exploration Constant",
            parent=self.MCTSGroup,
        )

        self.numIterCard = RangeSettingCard(
            cfg.numIter,
            FluentIcon.SETTING,
            "Iteration Times",
            parent=self.MCTSGroup,
        )

        self.useGPUCard = SwitchSettingCard(
            FluentIcon.SPEED_HIGH,
            "Use GPU as Accelerator",
            "Using GPU can speed up the thinking of Alpha Gobang (if available)",
            cfg.useGPU,
            parent=self.MCTSGroup,
        )

        self.MCTSGroup.addSettingCard(self.cPuctCard)
        self.MCTSGroup.addSettingCard(self.numIterCard)
        self.MCTSGroup.addSettingCard(self.useGPUCard)

        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(20, 10, 20, 20)

        self.expandLayout.addWidget(self.settingsLabel)
        self.expandLayout.addWidget(self.AppearanceGroup)
        self.expandLayout.addWidget(self.musicInThisPCGroup)
        self.expandLayout.addWidget(self.MCTSGroup)

        self.resize(1200, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self.__setQss()
        self.__connectSignalToSlot()

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(self.__onThemeChanged)

        self.modelFolderCard.clicked.connect(self.__onModelFolderCardClicked)
        self.cPuctCard.valueChanged.connect(self.__onMCTSChanged)
        self.numIterCard.valueChanged.connect(self.__onMCTSChanged)
        self.useGPUCard.checkedChanged.connect(self.__onMCTSChanged)

        self.cPuctCard.slider.sliderReleased.connect(self.__showSuccessTooltip)
        self.numIterCard.slider.sliderReleased.connect(self.__showSuccessTooltip)
        self.useGPUCard.checkedChanged.connect(self.__showSuccessTooltip)

    def __setQss(self):
        """ set style sheet """
        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.scrollWidget.setStyleSheet(
            "QWidget {background:transparent} QLabel#settingLabel { font: 33px 'Microsoft YaHei Light'}")

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.warning(
            '',
            'Configuration takes effect after restart',
            parent=self.window()
        )

    def __showSuccessTooltip(self):
        InfoBar.success(
            'Settings Applied',
            'Configuration has taken effect',
            parent=self.window()
        )

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

    def __onModelFolderCardClicked(self):
        """ download path card clicked slot """
        path = QFileDialog.getOpenFileName(
            self, "Choose Model File", "./", "Model (*.pth)")
        if not path[0] or cfg.get(cfg.modelPath) == path:
            return

        cfg.set(cfg.modelPath, path[0])
        self.modelFolderCard.setContent(path[0])
        self.__onMCTSChanged()
        self.__showSuccessTooltip()

    def __onMCTSChanged(self):
        self.MCTSRefreshSignal.emit()
