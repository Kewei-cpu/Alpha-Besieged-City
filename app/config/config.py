# coding:utf-8
from enum import Enum

from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            EnumSerializer)


class BoardBackgroundColorEnum(Enum):
    """ Board background enumeration class """

    PoliteRumors = "PoliteRumors"
    SpringWarmth = "SpringWarmth"
    SunnyMorning = "SunnyMorning"
    MorpheusDen = "MorpheusDen"
    EternalConstance = "EternalConstance"

    @classmethod
    def values(cls):
        return [q.value for q in cls]


class BoardGridColorEnum(Enum):
    SaintPetersburg = "SaintPetersburg"
    HeavyRain = "HeavyRain"
    MidnightBloom = "MidnightBloom"
    ViciousStance = "ViciousStance"

    @classmethod
    def values(cls):
        return [q.value for q in cls]


class Config(QConfig):
    """ Config of application """

    modelPath = ConfigItem(
        "Model", "ModelPath", "")

    cPuct = RangeConfigItem(
        "MonteCarloTree", "CPuct", 4, RangeValidator(1, 10))
    numIter = RangeConfigItem(
        "MonteCarloTree", "NumIter", 1000, RangeValidator(100, 10000))
    useGPU = ConfigItem(
        "MonteCarloTree", "UseGPU", True, BoolValidator())

    boardBackground = OptionsConfigItem(
        "Board", "BackgroundColor", BoardBackgroundColorEnum.PoliteRumors, OptionsValidator(BoardBackgroundColorEnum),
        EnumSerializer(BoardBackgroundColorEnum))
    boardBackgroundAlpha = RangeConfigItem(
        "Board", "BackgroundAlpha", 100, RangeValidator(0, 100)
    )
    boardGridColor = OptionsConfigItem(
        "Board", "GridColor", BoardGridColorEnum.SaintPetersburg, OptionsValidator(BoardGridColorEnum),
        EnumSerializer(BoardGridColorEnum))
    boardGridAlpha = RangeConfigItem(
        "Board", "GridAlpha", 100, RangeValidator(0, 100)
    )


#     # software update
#     checkUpdateAtStartUp = ConfigItem(
#         "Update", "CheckUpdateAtStartUp", True, BoolValidator())
#
#     @property
#     def desktopLyricFont(self):
#         """ get the desktop lyric font """
#         font = QFont(self.deskLyricFontFamily.value)
#         font.setPixelSize(self.deskLyricFontSize.value)
#         return font
#
#     @desktopLyricFont.setter
#     def desktopLyricFont(self, font: QFont):
#         dpi = QGuiApplication.primaryScreen().logicalDotsPerInch()
#         self.deskLyricFontFamily.value = font.family()
#         self.deskLyricFontSize.value = max(15, int(font.pointSize()*dpi/72))
#         self.save()


YEAR = 2024
AUTHOR = "kewei-cpu"
VERSION = "1.0.0"

FEEDBACK_URL = "https://github.com/kewei-cpu/Alpha-Besieged-City/issues"
RELEASE_URL = "https://github.com/kewei-cpu/Alpha-Besieged-City/releases/latest"

cfg = Config()
qconfig.load('app/config/config.json', cfg)
