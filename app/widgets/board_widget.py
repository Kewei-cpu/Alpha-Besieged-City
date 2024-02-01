import json
import os
import time

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QPainter, QGradient, QColor, QPen, QFont
from PySide6.QtWidgets import QFileDialog
from qfluentwidgets import InfoBar, FluentIcon, InfoBarPosition, StateToolTip, CardWidget, isDarkTheme

from alphazero import ChessBoard
from app.common import *
from app.config import *
from arena import *

# BLUE = (130, 175, 214)
BLUE = (60, 144, 217)
LIGHT_BLUE = tuple([int(255 - (255 - color) * 0.7) for color in BLUE])
DARK_BLUE = tuple([int(color * 0.7) for color in BLUE])
# GREEN = (80, 181, 142)
GREEN = (26, 177, 100)
LIGHT_GREEN = tuple([int(255 - (255 - color) * 0.5) for color in GREEN])
DARK_GREEN = tuple([int(color * 0.7) for color in GREEN])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class BoardWidget(CardWidget):
    onNotFirstMove = Signal(bool)
    onNotLastMove = Signal(bool)
    onSaveAvailable = Signal(bool)
    onSkipAvailable = Signal(bool)
    onHistoryChanged = Signal(list)
    onStepChanged = Signal(int)

    def __init__(self, routeKey, parent):
        super().__init__(parent)

        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)

        self.setObjectName(routeKey.replace(' ', '-'))

        self.screen_size = self.size().width(), self.size().height()
        self.board_len = 7
        self.border_size = 24
        self.board_size = min(self.screen_size[0], self.screen_size[1])
        self.grid_size = (self.board_size - 2 * self.border_size) / self.board_len
        self.padding_size = self.grid_size / 4
        self.margin_size = (self.screen_size[0] - self.board_size) / 2 + self.padding_size

        self.board = ChessBoard(self.board_len)
        self.active_player_pos_index = 0
        self.running = True
        self.mouse_pos = (0, 0)

        self.robot = None

        self.MCTS_enabled = False
        self.aiThread = None
        self.isAIThinking = False
        self.stateTooltip = None

        self.blue_final_territory = []
        self.green_final_territory = []

        self.history = []
        self.current_step = 0

        self.all_games = []

    def updateBoardSize(self):
        self.screen_size = self.size().width(), self.size().height()
        self.board_len = 7
        self.border_size = 20
        self.board_size = min(self.screen_size)
        self.grid_size = (self.board_size - 2 * self.border_size) / self.board_len
        self.padding_size = self.grid_size / 4
        self.margin_size = (round((self.screen_size[0] - self.board_size) / 2 + self.border_size, 0),
                            round((self.screen_size[1] - self.board_size) / 2 + self.border_size, 0))

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.updateBoardSize()

        self.drawBackground(painter)
        self.drawBoard(painter)
        self.drawCoordinate(painter)
        self.drawWall(painter)

        if self.running:
            self.drawAvailablePositions(painter)
            self.drawPlayers(painter)
            self.drawActivePlayer(painter)

            if not self.isAIThinking:
                self.drawActionPreview(painter)
        else:
            self.drawFinalTerritory(painter)
            self.drawDeadPlayer(painter)

        self.refreshSignal()

    def drawBackground(self, painter):
        painter.setPen(Qt.NoPen)
        grad = QGradient(eval("QGradient.Preset." + cfg.get(cfg.boardBackground).value))
        alpha = cfg.get(cfg.boardBackgroundAlpha)
        stops = grad.stops()
        for stop in stops:
            stop[1].setAlphaF(alpha / 100.0)
        grad.setStops(stops)
        painter.setBrush(grad)
        painter.drawRoundedRect(0, 0, self.screen_size[0], self.screen_size[1], 5, 5)

    def drawBoard(self, painter):
        painter.setPen(Qt.NoPen)
        grad = QGradient(eval("QGradient.Preset." + cfg.get(cfg.boardGridColor).value))
        alpha = cfg.get(cfg.boardGridAlpha)
        stops = grad.stops()
        for stop in stops:
            stop[1].setAlphaF(alpha / 100.0)
        grad.setStops(stops)
        painter.setBrush(grad)
        for i in range(self.board_len):
            for j in range(self.board_len):
                painter.drawRoundedRect(
                    self.margin_size[0] + j * self.grid_size + self.padding_size / 2,
                    self.margin_size[1] + i * self.grid_size + self.padding_size / 2,
                    self.grid_size - self.padding_size,
                    self.grid_size - self.padding_size,
                    5,
                    5
                )

    def drawCoordinate(self, painter):
        if not cfg.get(cfg.showCoordinate):
            return

        if isDarkTheme():
            painter.setPen(QPen(QColor(*WHITE, 140), 1))
        else:
            painter.setPen(QPen(QColor(*BLACK, 140), 1))

        if self.board_size >= 600:
            painter.setFont(QFont("Microsoft YaHei", 12))
        else:
            painter.setFont(QFont("Microsoft YaHei", 10))

        for i in range(self.board_len):
            painter.drawText(
                self.margin_size[0] + (i + 0.5) * self.grid_size - 5,
                self.board_size + self.margin_size[1] - 30,
                chr(i + 97)
            )
            painter.drawText(
                self.margin_size[0] - 13,
                self.margin_size[1] + (i + 0.5) * self.grid_size + 4,
                str(self.board_len - i)
            )

    def drawPlayers(self, painter):
        """
        绘制玩家
        :param scr:屏幕
        :return:
        """

        painter.setPen(Qt.NoPen)
        painter.setBrush(QGradient(QGradient.Preset.FlyHigh))
        painter.drawEllipse(
            self.margin_size[0] + (self.board.player_pos[0][1] + 0.25) * self.grid_size,
            self.margin_size[1] + (self.board.player_pos[0][0] + 0.25) * self.grid_size,
            self.grid_size * 0.5,
            self.grid_size * 0.5,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(QGradient(QGradient.Preset.GrownEarly))
        painter.drawEllipse(
            self.margin_size[0] + (self.board.player_pos[1][1] + 0.25) * self.grid_size,
            self.margin_size[1] + (self.board.player_pos[1][0] + 0.25) * self.grid_size,
            self.grid_size * 0.5,
            self.grid_size * 0.5,
        )

    def drawActivePlayer(self, painter):
        """
        绘制当前玩家（深色外框）
        :param scr: 屏幕
        :return:
        """
        if self.board.state[12, 0, 0] == 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QGradient(QGradient.Preset.Seashore))
            painter.drawEllipse(
                self.margin_size[0] + (self.board.player_pos[0][1] + 0.25) * self.grid_size,
                self.margin_size[1] + (self.board.player_pos[0][0] + 0.25) * self.grid_size,
                self.grid_size * 0.5,
                self.grid_size * 0.5,
            )

        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QGradient(QGradient.Preset.NewLife))
            painter.drawEllipse(
                self.margin_size[0] + (self.board.player_pos[1][1] + 0.25) * self.grid_size,
                self.margin_size[1] + (self.board.player_pos[1][0] + 0.25) * self.grid_size,
                self.grid_size * 0.5,
                self.grid_size * 0.5,
            )

    def drawDeadPlayer(self, painter):
        """
        显示死亡玩家
        :param scr: 屏幕
        :return:
        """
        painter.setBrush(QColor(*WHITE, 0))

        painter.setPen(QPen(QColor(*DARK_BLUE, 255), self.grid_size / 20))
        painter.drawEllipse(
            self.margin_size[0] + (self.board.player_pos[0][1] + 0.25) * self.grid_size,
            self.margin_size[1] + (self.board.player_pos[0][0] + 0.25) * self.grid_size,
            self.grid_size * 0.5,
            self.grid_size * 0.5,
        )

        painter.setPen(QPen(QColor(*DARK_GREEN, 255), self.grid_size / 20))
        painter.drawEllipse(
            self.margin_size[0] + (self.board.player_pos[1][1] + 0.25) * self.grid_size,
            self.margin_size[1] + (self.board.player_pos[1][0] + 0.25) * self.grid_size,
            self.grid_size * 0.5,
            self.grid_size * 0.5,
        )

    def drawActionPreview(self, painter: QPainter):
        """
        显示动作预览（跟随鼠标）
        :param scr: 屏幕
        :return:
        """
        pos_x, pos_y = self.mouse_pos

        if self.mouse_pos_to_action(pos_x, pos_y) not in self.board.available_actions:
            return

        move = self.board.action_to_pos[self.mouse_pos_to_action(pos_x, pos_y) // 4]
        wall = self.mouse_pos_to_action(pos_x, pos_y) % 4

        destination = (self.board.player_pos[int(self.board.state[12, 0, 0])][0] + move[0],
                       self.board.player_pos[int(self.board.state[12, 0, 0])][1] + move[1])

        active_player_color = BLUE if self.board.state[12, 0, 0] == 0 else GREEN

        if wall == 0:
            self.drawHorizontalWall(painter, active_player_color, destination[0] - 1, destination[1])
        elif wall == 1:
            self.drawVerticalWall(painter, active_player_color, destination[0], destination[1] - 1)
        elif wall == 2:
            self.drawHorizontalWall(painter, active_player_color, destination[0], destination[1])
        elif wall == 3:
            self.drawVerticalWall(painter, active_player_color, destination[0], destination[1])

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(*active_player_color, 180))
        painter.drawEllipse(
            self.margin_size[0] + (destination[1] + 0.25) * self.grid_size,
            self.margin_size[1] + (destination[0] + 0.25) * self.grid_size,
            self.grid_size * 0.5,
            self.grid_size * 0.5,
        )

    def drawAvailablePositions(self, painter):
        """
        显示可移动位置
        :param scr: 屏幕
        :return:
        """

        available_positions = []
        light_color = BLUE if self.board.state[12, 0, 0] == 0 else GREEN

        for action in self.board.available_actions:
            pos = (
                self.board.action_to_pos[action // 4][0] +
                self.board.player_pos[int(self.board.state[12, 0, 0])][0],
                self.board.action_to_pos[action // 4][1] +
                self.board.player_pos[int(self.board.state[12, 0, 0])][1]
            )
            if pos not in available_positions:
                available_positions.append(pos)

        for pos in available_positions:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(*light_color, 100))
            ## draw a small circle at the center of the grid
            painter.drawEllipse(
                self.margin_size[0] + (pos[1] + 0.35) * self.grid_size,
                self.margin_size[1] + (pos[0] + 0.35) * self.grid_size,
                self.grid_size * 0.3,
                self.grid_size * 0.3,
            )

    def drawFinalTerritory(self, painter: QPainter):
        """
        显示最终领地（游戏结束后）
        :param scr: 屏幕
        :return:
        """
        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(*LIGHT_BLUE, 100))
        for pos in self.blue_final_territory:
            painter.drawRoundedRect(
                self.margin_size[0] + pos[1] * self.grid_size + self.padding_size / 2,
                self.margin_size[1] + pos[0] * self.grid_size + self.padding_size / 2,
                self.grid_size - self.padding_size,
                self.grid_size - self.padding_size,
                5,
                5
            )

        painter.setBrush(QColor(*LIGHT_GREEN, 100))
        for pos in self.green_final_territory:
            painter.drawRoundedRect(
                self.margin_size[0] + pos[1] * self.grid_size + self.padding_size / 2,
                self.margin_size[1] + pos[0] * self.grid_size + self.padding_size / 2,
                self.grid_size - self.padding_size,
                self.grid_size - self.padding_size,
                5,
                5
            )

    def drawWall(self, painter: QPainter):
        """
        绘制墙
        :param painter:
        :param scr: 屏幕
        :return:
        """
        if cfg.get(cfg.boardGridColor) in (BoardGridColorEnum.SaintPetersburg, BoardGridColorEnum.HeavyRain):
            color = WHITE
        else:
            color = BLACK

        for i in range(self.board_len):
            for j in range(self.board_len):
                if self.board.state[6, i, j] == 1:
                    self.drawHorizontalWall(painter, color, i, j)
                if self.board.state[9, i, j] == 1:
                    self.drawVerticalWall(painter, color, i, j)

    def drawHorizontalWall(self, painter: QPainter, color, pos_y, pos_x, width=0):
        """
        绘制水平墙
        :param scr: 屏幕
        :param color: 颜色
        :param pos_y: 纵坐标
        :param pos_x: 横坐标
        :param width: 外框宽度 0为填充
        :return:
        """
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(*color, 120))
        painter.drawPolygon(
            (QPoint(self.margin_size[0] + pos_x * self.grid_size,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size),
             QPoint(self.margin_size[0] + pos_x * self.grid_size + self.padding_size // 4,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size + self.padding_size // 4),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size + self.padding_size // 4),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size - self.padding_size // 4),
             QPoint(self.margin_size[0] + pos_x * self.grid_size + self.padding_size // 4,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size - self.padding_size // 4),)
        )

    def drawVerticalWall(self, painter: QPainter, color, pos_y, pos_x, width=0):
        """
        绘制垂直墙
        :param scr: 屏幕
        :param color: 颜色
        :param pos_y: 纵坐标
        :param pos_x: 横坐标
        :param width: 外框宽度 0为填充
        :return:
        """

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(*color, 120))
        painter.drawPolygon(
            (QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size,
                    self.margin_size[1] + pos_y * self.grid_size),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size + self.padding_size // 4,
                    self.margin_size[1] + pos_y * self.grid_size + self.padding_size // 4),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size + self.padding_size // 4,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size - self.padding_size // 4),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                    self.margin_size[1] + (pos_y + 1) * self.grid_size - self.padding_size // 4),
             QPoint(self.margin_size[0] + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                    self.margin_size[1] + pos_y * self.grid_size + self.padding_size // 4),)
        )

    def mouse_pos_to_action(self, mouse_pos_x, mouse_pos_y):
        """
        将鼠标位置转换为动作
        :param mouse_pos_y: 鼠标位置 y
        :param mouse_pos_x: 鼠标位置 x
        :return: 动作（0-99整数）
        """

        grid_y = (mouse_pos_y - self.margin_size[1]) // self.grid_size
        grid_x = (mouse_pos_x - self.margin_size[0]) // self.grid_size

        active_pos = self.board.player_pos[int(self.board.state[12, 0, 0])]

        move = grid_y - active_pos[0], grid_x - active_pos[1]

        internal_y = (mouse_pos_y - self.margin_size[1]) % self.grid_size
        internal_x = (mouse_pos_x - self.margin_size[0]) % self.grid_size

        if internal_x > internal_y:
            wall = 3 if internal_x > self.grid_size - internal_y else 0
        else:
            wall = 2 if internal_x > self.grid_size - internal_y else 1

        try:
            action = self.board.pos_to_action[move] * 4 + wall
        except KeyError:
            return None

        return action

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.stateTooltip:
            self.stateTooltip.move(self.window().width() - self.stateTooltip.width() - 75, 10)
            self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.mouse_pos = event.x(), event.y()
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.buttons() == Qt.LeftButton:
            if not self.running:
                return
            if self.isAIThinking:
                return

            action = self.mouse_pos_to_action(event.x(), event.y())
            s = self.doAction(action)
            self.update()

            if s and self.running:
                if self.robot is not None:
                    self.robotMove()
                if self.MCTS_enabled:
                    self.nnMove()

    def refreshBoard(self):
        self.board.clear_board()
        self.running = True
        self.active_player_pos_index = 0
        self.blue_final_territory = []
        self.green_final_territory = []
        for action in self.history[:self.current_step]:
            self.doAction(action, False)
        self.onStepChanged.emit(self.current_step)
        self.update()

    def onRestart(self):
        if self.isAIThinking:
            return

        self.current_step = 0
        self.history = []
        self.refreshBoard()

    def onPrevious(self):
        self.setCurrentStep(self.current_step - 1)

    def onNext(self):
        self.setCurrentStep(self.current_step + 1)

    def onFirst(self):
        self.setCurrentStep(0)

    def onLast(self):
        self.setCurrentStep(len(self.history))

    def setCurrentStep(self, index):
        if self.isAIThinking:
            return

        self.current_step = index
        self.refreshBoard()

    def onSave(self):
        if not self.history:
            InfoBar.error(
                title="Save Failed",
                content="Can't save empty game!",
                parent=self)
            return

        os.makedirs('./games', exist_ok=True)
        t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        is_over, winner = self.board.is_game_over()
        if is_over:
            if winner == 0:
                result = "Blue Win"
            elif winner == 1:
                result = "Green Win"
            else:
                result = "Draw"
        else:
            result = "Unfinished"

        with open(f'./games/game_{t}.abc', 'w', encoding='utf-8') as f:
            game_dict = {
                "Time": t,
                "Moves": self.history,
                "Move Count": len(self.history),
                "Result": result
            }
            json.dump(game_dict, f)

        InfoBar.success(
            title="Game Saved",
            content=f"Game saved to log/board/",
            parent=self.parent().parent(),
        )

    def onLoad(self):
        if self.isAIThinking:
            return

        path = QFileDialog.getOpenFileName(
            self, "Choose Game File", "games", "Alpha Besieged City Game (*.abc)")

        if not path[0]:
            return

        with open(path[0], 'r', encoding='utf-8') as f:
            game_dict = json.load(f)
            try:
                self.history = game_dict["Moves"]
                self.onHistoryChanged.emit(self.history)
                self.current_step = 0
                self.refreshBoard()
            except Exception:
                InfoBar.error(
                    title="Load Failed",
                    content="Can't load this game!",
                    duration=2000,
                    parent=self.parent().parent()
                )
            else:
                InfoBar.success(
                    title="Load Successfully",
                    content=f"Loaded game with {len(self.history)} moves",
                    duration=2000,
                    parent=self.parent().parent(),
                )

    def onSelectRobot(self, text):
        if text == "Random":
            self.robot = Random(self.board)
        elif text == "Max Territory":
            self.robot = MaxTerritory(self.board)
        elif text == "Max Sigmoid Territory":
            self.robot = MaxSigmoidTerritory(self.board, K=2, B=2)
        elif text == "Max Diff Sigmoid Territory":
            self.robot = MaxDiffSigmoidTerritory(self.board, K=2, B=2)
        elif text == "Max Percent Sigmoid Territory":
            self.robot = MaxPercentSigmoidTerritory(self.board, K=2, B=2)

    def onEnableMCTS(self):
        self.aiThread = AIThread(
            chessBoard=self.board,
            parent=self
        )
        signalBus.modelChanged.connect(self.onRefreshMCTS)
        self.aiThread.searchComplete.connect(self.onSearchComplete)
        self.MCTS_enabled = True

    def onRefreshMCTS(self):
        if self.isAIThinking:
            return
        if not self.MCTS_enabled:
            return

        self.aiThread = AIThread(
            chessBoard=self.board,
            parent=self
        )
        self.aiThread.searchComplete.connect(self.onSearchComplete)

    def closeEvent(self, e):
        """ 关闭界面 """
        self.aiThread.quit()
        self.aiThread.wait()
        self.aiThread.deleteLater()
        e.accept()

    def createGameOverInfoBar(self, title, content, color):
        w = InfoBar.new(
            icon=FluentIcon.COMPLETED,
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.parent().parent()
        )
        w.setCustomBackgroundColor(color, color)

    def doAction(self, action, change_history=True):
        """
        执行动作
        :param action: 动作（0-99整数）
        :return:
        """
        if action not in self.board.available_actions:
            return False

        self.board.do_action(action)

        if change_history:
            self.history = self.history[:self.current_step]
            self.history.append(action)
            self.current_step += 1
            self.onHistoryChanged.emit(self.history)
            self.onStepChanged.emit(self.current_step)

        if self.board.is_game_over_()[0]:
            self.running = False

            self.blue_final_territory = self.board.is_game_over_()[1]
            self.green_final_territory = self.board.is_game_over_()[2]

            self.all_games.append(self.history)

            self.print_result()

        self.active_player_pos_index = 0 if self.board.state[12, 0, 0] == 0 else 3

        return True

    def robotMove(self):
        if not self.running:
            return

        move = self.robot.play()
        self.doAction(move)
        self.update()

    def refreshSignal(self):
        self.onNotFirstMove.emit(self.current_step > 0)
        self.onNotLastMove.emit(self.current_step < len(self.history))
        self.onSaveAvailable.emit(len(self.history) > 0)
        self.onSkipAvailable.emit(self.robot is not None or self.MCTS_enabled)

    def nnMove(self):
        """ 获取 AI 的动作 """
        if self.isAIThinking:
            return

        self.stateTooltip = StateToolTip(
            title='AI is thinking',
            content='Please wait a moment',
            parent=self.parent().parent()
        )
        self.stateTooltip.move(self.window().width() - self.stateTooltip.width() - 85, 10)
        self.stateTooltip.raise_()
        self.stateTooltip.show()

        self.isAIThinking = True
        self.aiThread.start()

    def onSearchComplete(self, action: int):
        """ AI 思考完成槽函数 """
        self.stateTooltip.setState(True)
        self.isAIThinking = False
        self.stateTooltip = None
        self.doAction(action)
        self.update()

    def print_result(self):
        """
        打印游戏结果
        :return:
        """
        blue_score = len(self.board.is_game_over_()[1])
        green_score = len(self.board.is_game_over_()[2])

        title = ""
        content = ""

        if blue_score > green_score:
            title += "BLUE WIN!"
            color = QColor(*LIGHT_BLUE)
        elif blue_score < green_score:
            title += "GREEN WIN!"
            color = QColor(*LIGHT_GREEN)
        else:
            title += "DRAW!"
            color = "white"

        content += f"BLUE:{blue_score}, GREEN:{green_score}"

        self.createGameOverInfoBar(title, content, color)
