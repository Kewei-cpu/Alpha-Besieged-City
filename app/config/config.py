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



    cPuct = RangeConfigItem(
        "MonteCarloTree", "CPuct", 4, RangeValidator(4, 10))
    numIter = RangeConfigItem(
        "MonteCarloTree", "NumIter", 1000, RangeValidator(100, 10000))
    useGPU = ConfigItem(
        "MonteCarloTree", "UseGPU", True, BoolValidator())
    modelPath = ConfigItem(
        "MonteCarloTree", "ModelPath", "")


    enableAcrylicBackground = ConfigItem(
        "MainWindow", "EnableAcrylicBackground", False, BoolValidator())

    boardBackground = OptionsConfigItem(
        "Board", "BackgroundColor", BoardBackgroundColorEnum.SunnyMorning, OptionsValidator(BoardBackgroundColorEnum),
        EnumSerializer(BoardBackgroundColorEnum))
    boardBackgroundAlpha = RangeConfigItem(
        "Board", "BackgroundAlpha", 20, RangeValidator(0, 100)
    )
    boardGridColor = OptionsConfigItem(
        "Board", "GridColor", BoardGridColorEnum.ViciousStance, OptionsValidator(BoardGridColorEnum),
        EnumSerializer(BoardGridColorEnum))
    boardGridAlpha = RangeConfigItem(
        "Board", "GridAlpha", 20, RangeValidator(0, 100)
    )



YEAR = 2024
AUTHOR = "kewei-cpu"
VERSION = "1.0.0"

FEEDBACK_URL = "https://github.com/kewei-cpu/Alpha-Besieged-City/issues"
RELEASE_URL = "https://github.com/kewei-cpu/Alpha-Besieged-City/releases/latest"

cfg = Config()
qconfig.load('config/config.json', cfg)
