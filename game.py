# coding:utf-8
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import *

from app.view import *


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = HomeInterface('Home Interface', self)
        self.boardInterfaceFriend = PlayFriendInterface('Player with Friends', self)
        self.boardInterfaceRobot = PlayRobotInterface('Player with Robots', self)
        self.boardInterfaceNN = PlayNNInterface('Player with Neural Network', self)

        self.settingInterface = Widget('Setting Interface', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, 'Home')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.boardInterfaceFriend, FluentIcon.PEOPLE, 'Player with Friends',
                             NavigationItemPosition.SCROLL)
        self.addSubInterface(self.boardInterfaceRobot, FluentIcon.ROBOT, 'Player with Robots',
                             NavigationItemPosition.SCROLL)
        self.addSubInterface(self.boardInterfaceNN, FluentIcon.EDUCATION, 'Player with Neural Network',
                             NavigationItemPosition.SCROLL)
        # add custom widget to bottom
        # self.navigationInterface.addWidget(
        #     routeKey='avatar',
        #     widget=NavigationAvatarWidget('zhiyiYo', 'resource/shoko.png'),
        #     onClick=self.showMessageBox,
        #     position=NavigationItemPosition.BOTTOM,
        # )

        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # add badge to navigation item
        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('../../resources/icon/bluegreen.png'))
        self.setWindowTitle('Alpha Besieged City')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # set the minimum window width that allows the navigation panel to be expanded
        # self.navigationInterface.setMinimumExpandWidth(900)
        # self.navigationInterface.expand(useAni=False)

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
