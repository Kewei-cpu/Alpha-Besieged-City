# coding: utf-8
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from qfluentwidgets import *


class SettingInterface(ScrollArea):
    enableAcrylicChanged = Signal(bool)

    def __init__(self, text, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(text.replace(' ', '-'))

        # 默认配置
        self.config = {
            "c_puct": 4,
            "is_use_gpu": True,
            "n_mcts_iters": 1500,
            "is_human_first": True,
            "is_enable_acrylic": True,
            "model": "model/history/best_policy_value_net_4400.pth"
        }
        # 读入用户配置
        self.__readConfig()

        self.view = QWidget(self)

        self.expandLayout = ExpandLayout(self.view)

        self.settingsLabel = TitleLabel('Settings', self.view)
        self.settingsLabel.setFixedHeight(80)
        # self.settingsLabel.setObjectName('settingLabel')

        self.musicInThisPCGroup = SettingCardGroup(
            "Alpha Besieged City on this PC", self.view)

        self.downloadFolderCard = PushSettingCard(
            'Choose folder',
            FluentIcon.DOWNLOAD,
            "Model directory",
            '123',
            self.musicInThisPCGroup
        )

        self.MCTSGroup = SettingCardGroup(
            "MCTS", self.view)

        # self.cPuctCard = RangeSettingCard(
        #     'Exploration constant',
        #     FluentIcon.SETTING,
        #     'c_puct',
        #     self.config['c_puct'].__str__(),
        #     self.MCTSGroup
        # )




        self.musicInThisPCGroup.addSettingCard(self.downloadFolderCard)



        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(20, 20, 20, 30)

        self.expandLayout.addWidget(self.settingsLabel)
        self.expandLayout.addWidget(self.musicInThisPCGroup)

        self.resize(1200, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.__setQss()

    def __setQss(self):
        """ set style sheet """
        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet(
            "QWidget {background:transparent} QLabel#settingLabel { font: 33px 'Microsoft YaHei Light'}")

    def __readConfig(self):
        """ 读入配置 """
        self.__checkDir()
        try:
            with open('app/config/config.json', encoding='utf-8') as f:
                self.config.update(json.load(f))
        except:
            pass

    def __checkDir(self):
        """ 检查配置文件夹是否存在 """
        if not os.path.exists('app/config'):
            os.mkdir('app/config')

    def __showSelectModelDialog(self):
        """ 显示选择模型对话框 """
        w = SelectModelDialog(self.config['model'], self.window())
        w.modelChangedSignal.connect(self.__onModelChanged)
        w.exec_()

    def __onModelChanged(self, model: str):
        """ 模型改变信号槽函数 """
        if model != self.config['model']:
            self.config['model'] = model

    def __onEnableAcrylicChanged(self, isEnableAcrylic: bool):
        """ 使用亚克力背景开关按钮的开关状态变化槽函数 """
        self.config['is_enable_acrylic'] = isEnableAcrylic
        self.acrylicSwitchButton.setText(
            'On' if isEnableAcrylic else 'Off')
        self.enableAcrylicChanged.emit(isEnableAcrylic)

    def __onUseGPUChanged(self, isUseGPU: bool):
        """ 使用 GPU 加速开关按钮的开关状态改变槽函数 """
        self.config['is_use_gpu'] = isUseGPU
        self.useGPUSwitchButton.setText(
            'On' if isUseGPU else 'Off')

    def __onFirstHandChanged(self):
        """ 先手改变 """
        self.config['is_human_first'] = self.humanButton.isChecked()

    def __onCPuctChanged(self, cPuct: float):
        """ 调整探索常数槽函数 """
        self.config['c_puct'] = cPuct / 10
        self.cPuctValueLabel.setText(str(cPuct / 10))

    def __onMctsIterTimesChanged(self, iterTime: int):
        """ 调整蒙特卡洛树搜索次数槽函数 """
        self.config['n_mcts_iters'] = iterTime
        self.mctsIterTimeValueLabel.setNum(iterTime)

    def saveConfig(self):
        """ 保存设置 """
        self.__checkDir()
        with open('app/config/config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f)
