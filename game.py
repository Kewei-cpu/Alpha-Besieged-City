# coding:utf-8
import ctypes
import os
import sys

from PySide6.QtCore import QUrl, QEventLoop, QTimer, QSize
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication
from qfluentwidgets import SplashScreen, FluentIcon, NavigationItemPosition, MessageBox, isDarkTheme, \
    MSFluentWindow

from app.common import *
from app.view import *

base_dir = os.path.dirname(os.path.abspath(__file__))
import resources.resources


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()



        # create sub interface
        self.homeInterface = HomeInterface('Home', self)
        self.playInterface = PlayInterface('Play', self)
        self.settingInterface = SettingInterface('Setting', self)

        self.initNavigation()
        self.initWindow()
        self.connectSignalToSlot()

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))

        self.show()

        self.createSubInterface()
        self.splashScreen.finish()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, 'Home')
        self.addSubInterface(self.playInterface, MyFluentIcon.GRID, 'Play')

        # add custom widget to bottom
        # self.navigationInterface.addWidget(
        #     routeKey='avatar',
        #     widget=NavigationAvatarWidget('zhiyiYo', ':/logo/icon.png'),
        #     onClick=self.showMessageBox,
        #     position=NavigationItemPosition.BOTTOM,
        # )

        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings',
                             position=NavigationItemPosition.BOTTOM)

    def initWindow(self):

        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/logo/icon.ico'))
        self.setWindowTitle('Alpha Besieged City')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1500, loop.quit)
        loop.exec()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def showMessageBox(self):
        box = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        box.yesButton.setText('来啦老弟')
        box.cancelButton.setText('下次一定')

        if box.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))

    def setMicaEffectEnabled(self, isEnabled: bool):
        """ set whether the mica effect is enabled, only available on Win11 """
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())


if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QApplication(sys.argv)
    w = Window()
    app.exec()
