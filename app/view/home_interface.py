# coding:utf-8
import sys, os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import *

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class StatisticsWidget(QWidget):
    """ Statistics widget """

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.valueLabel.setAlignment(Qt.AlignCenter)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))


class AppInfoCard(SimpleCardWidget):
    """ App information card """

    def __init__(self, parent=None):
        super().__init__(parent)
        from game import base_dir
        self.iconLabel = ImageLabel(os.path.join(base_dir, 'resources', 'icon', 'icon.png'), self)
        self.iconLabel.scaledToWidth(160)

        self.nameLabel = TitleLabel('Alpha Besieged City', self)
        self.installButton = HyperlinkButton('https://github.com/Kewei-cpu/Alpha-Besieged-City', 'Github Page', self,
                                             FluentIcon.GITHUB)
        self.companyLabel = HyperlinkLabel(
            QUrl('https://github.com/Kewei-cpu'), 'Keweijun', self)
        self.installButton.setFixedWidth(160)

        self.scoreWidget = StatisticsWidget('Star', '1', self)
        self.separator = VerticalSeparator(self)
        self.commentWidget = StatisticsWidget('Fork', '1', self)

        self.descriptionLabel = BodyLabel(
            'A novel two-player board game. Your goal is to get the maximum territory and win. Detailed rules can be found bolow. Several AI models are also integrated.',
            self)
        self.descriptionLabel.setWordWrap(True)

        # self.tagButton = PillPushButton('组件库', self)
        # self.tagButton.setCheckable(False)
        # setFont(self.tagButton, 12)
        # self.tagButton.setFixedSize(80, 32)
        #
        # self.shareButton = TransparentToolButton(FluentIcon.SHARE, self)
        # self.shareButton.setFixedSize(32, 32)
        # self.shareButton.setIconSize(QSize(14, 14))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        # self.buttonLayout = QHBoxLayout()

        self.initLayout()

    def initLayout(self):
        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        # name label and install button
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.addWidget(self.nameLabel)
        self.topLayout.addWidget(self.installButton, 0, Qt.AlignRight)

        # company label
        self.vBoxLayout.addSpacing(3)
        self.vBoxLayout.addWidget(self.companyLabel)

        # statistics widgets
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addLayout(self.statisticsLayout)
        self.statisticsLayout.setContentsMargins(0, 0, 0, 0)
        self.statisticsLayout.setSpacing(10)
        self.statisticsLayout.addWidget(self.scoreWidget)
        self.statisticsLayout.addWidget(self.separator)
        self.statisticsLayout.addWidget(self.commentWidget)
        self.statisticsLayout.setAlignment(Qt.AlignLeft)

        # description label
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.descriptionLabel)

        # # button
        # self.vBoxLayout.addSpacing(12)
        # self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        # self.vBoxLayout.addLayout(self.buttonLayout)
        # self.buttonLayout.addWidget(self.tagButton, 0, Qt.AlignLeft)
        # self.buttonLayout.addWidget(self.shareButton, 0, Qt.AlignRight)


class DescriptionCard(HeaderCardWidget):
    """ Description card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Rules')
        setFont(self.headerLabel, 22, QFont.DemiBold)

        self.contentLayout = QVBoxLayout()

        self.gameLabel = BodyLabel('Game Board', self)
        setFont(self.gameLabel, 18, QFont.DemiBold)
        self.contentLayout.addWidget(self.gameLabel)

        text = """<ul style="list-style:circle;margin-left:-1.5em;">
<li>The game board is officially a <b>7x7 grid</b>, but you can change it to any size you want.
<li>This game if played with 2 players. <strong>Player Blue</strong> is started on the left top corner, and <strong>Player Green</strong> is started on the right bottom corner.
        """

        self.descriptionLabel = BodyLabel(text, self)
        setFont(self.descriptionLabel, 16)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setContentsMargins(0, 0, 0, 10)
        self.contentLayout.addWidget(self.descriptionLabel)
        self.contentLayout.addWidget(HorizontalSeparator(self))

        self.gameLabel = BodyLabel('Move and Place', self)
        setFont(self.gameLabel, 18, QFont.DemiBold)
        self.contentLayout.addWidget(self.gameLabel)

        text = """<ul style="list-style:circle;margin-left:-1.5em;">
        <li><b>Player Blue</b> goes first, then two player go in turn. Each turn, a player move his/her pieces, and place a new wall on the board.
        <li>A <b>step</b> is defined as moving a piece to a neighboring grid (up, down, left, right) that is not occupied by another piece or blocked by a wall.
        <li>A legal move can include <b>0~3 steps</b>, which means the player can stay in the same grid.
        <li>After move, the player <b>MUST</b> place a wall on the board. The wall can only be placed on one of the <b>four sides</b> of the grid that the player move to. Walls cannot be placed on another wall or on the outer edge of the board.
                """
        self.descriptionLabel = BodyLabel(text, self)
        setFont(self.descriptionLabel, 16)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setContentsMargins(0, 0, 0, 10)
        self.contentLayout.addWidget(self.descriptionLabel)
        self.contentLayout.addWidget(HorizontalSeparator(self))

        self.gameLabel = BodyLabel('Win or Lose', self)
        setFont(self.gameLabel, 18, QFont.DemiBold)
        self.contentLayout.addWidget(self.gameLabel)

        text = """<ul style="list-style:circle;margin-left:-1.5em;">
        <li>The game ends when two players' pieces are <b>completely seperated</b> by walls, which means one player cannot reach the other no matter how many steps he/she moves.
        <li>A player's territory is the number of grids that he/she can reach when the game ends. A grid that cannot be reached by any player is not counted as any player's territory.
        <li><b>The player with more territory wins.</b>
                """

        self.descriptionLabel = BodyLabel(text, self)
        setFont(self.descriptionLabel, 16)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setContentsMargins(0, 0, 0, 10)
        self.contentLayout.addWidget(self.descriptionLabel)

        self.viewLayout.addLayout(self.contentLayout)


class RobotInfoCard(HeaderCardWidget):
    """ Robot information card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Robot Information')
        setFont(self.headerLabel, 22, QFont.DemiBold)

        self.contentLayout = QVBoxLayout()

        self.gameLabel = BodyLabel('Max Territory Series', self)
        setFont(self.gameLabel, 18, QFont.DemiBold)
        self.contentLayout.addWidget(self.gameLabel)

        text = """Including 4 models: Max Territory, Max Sigmoid Territory, Max Diff Sigmoid Territory,  Max Percent Sigmoid Territory. The are all based on the same territory algorithm, but with different reward function. The first one is the original one, and the other three are based on the sigmoid function, which let them focus more on the general position rather than the specific territory. Currently, the <b>Max Diff Sigmoid Territory</b> model is considered the best one. You can try them all in <b>"Play with Robot"</b> and see which one is the best for you. """
        self.descriptionLabel = BodyLabel(text, self)
        setFont(self.descriptionLabel, 16)
        self.descriptionLabel.setContentsMargins(0, 0, 0, 10)
        self.descriptionLabel.setWordWrap(True)
        self.contentLayout.addWidget(self.descriptionLabel)
        self.contentLayout.addWidget(HorizontalSeparator(self))

        self.gameLabel = BodyLabel('MCTS', self)
        setFont(self.gameLabel, 18, QFont.DemiBold)
        self.contentLayout.addWidget(self.gameLabel)

        text = """MCTS is short for Monte Carlo Tree Search. It is a search algorithm that can be used in many games. It is based on the idea of random sampling. In this game, it is used to simulate the game and find the best move. The MCTS model is <b>generally better</b> than Max Territory models, but it is <b>much slower</b>. You can try it in <b>"Play with MCTS"</b> and see how it works. 
        <br>There are several options for MCTS that you can change in <b>"Settings"</b>:
        <ul style="list-style:circle;margin-left:-1.5em;margin-top:-10px">
        <li><b>Exploration Constant</b>: The exploration constant is used to balance the exploration and exploitation. There is no direct relationship between the value and the performance. You can try different values and see which one is the best for you. The default value is 4.
        <li><b>Number of Iterations</b>: The number of iterations is the number of simulations that the model will run. A higher value means the model will try more moves, which means it will be more accurate. A lower value means the model will try less moves, which means it will be faster. The default value is 1000.
        """
        self.descriptionLabel = BodyLabel(text, self)
        setFont(self.descriptionLabel, 16)
        self.descriptionLabel.setContentsMargins(0, 0, 0, 10)
        self.descriptionLabel.setWordWrap(True)
        self.contentLayout.addWidget(self.descriptionLabel)

        self.viewLayout.addLayout(self.contentLayout)




class HomeInterface(SingleDirectionScrollArea):

    def __init__(self, text, parent):
        super().__init__(parent)

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.appCard = AppInfoCard(self)
        # self.galleryCard = GalleryCard(self)
        self.descriptionCard = DescriptionCard(self)
        # self.systemCard = SystemRequirementCard(self)
        self.robotCard = RobotInfoCard(self)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName(text)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 30)
        self.vBoxLayout.addWidget(self.appCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.descriptionCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.robotCard, 0, Qt.AlignTop)

        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')
