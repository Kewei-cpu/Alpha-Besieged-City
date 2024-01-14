from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPainter, QGradient, QColor, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget
from qfluentwidgets import InfoBar, FluentIcon, InfoBarPosition

from alphazero import ChessBoard

BLUE = (130, 175, 214)
LIGHT_BLUE = tuple([int(255 - (255 - color) * 1) for color in BLUE])
DARK_BLUE = tuple([int(color * 0.7) for color in BLUE])
GREEN = (80, 181, 142)
LIGHT_GREEN = tuple([int(255 - (255 - color) * 0.9) for color in GREEN])
DARK_GREEN = tuple([int(color * 0.7) for color in GREEN])

WHITE = (255, 255, 255)


class BoardWidget(QWidget):
    def __init__(self, text, parent):
        super().__init__(parent)

        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)

        self.setObjectName(text.replace(' ', '-'))

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

        self.blue_final_territory = []
        self.green_final_territory = []
        self.history = []
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
        self.drawWall(painter)

        if self.running:
            self.drawAvailablePositions(painter)
            self.drawPlayers(painter)
            self.drawActivePlayer(painter)
            self.drawActionPreview(painter)
        else:
            self.drawFinalTerritory(painter)
            self.drawDeadPlayer(painter)

    def drawBackground(self, painter):
        painter.setPen(QColor(*WHITE, 0))
        painter.setBrush(QGradient(QGradient.Preset.PoliteRumors))
        painter.drawRoundedRect(0, 0, self.screen_size[0], self.screen_size[1], 5, 5)

    def drawBoard(self, painter):
        painter.setPen(QColor(*WHITE, 0))
        painter.setBrush(QGradient(QGradient.Preset.SaintPetersburg))
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

    def drawPlayers(self, painter):
        """
        绘制玩家
        :param scr:屏幕
        :return:
        """

        painter.setPen(QColor(*WHITE, 0))
        painter.setBrush(QGradient(QGradient.Preset.FlyHigh))
        painter.drawEllipse(
            self.margin_size[0] + (self.board.player_pos[0][1] + 0.25) * self.grid_size,
            self.margin_size[1] + (self.board.player_pos[0][0] + 0.25) * self.grid_size,
            self.grid_size * 0.5,
            self.grid_size * 0.5,
        )

        painter.setPen(QColor(*WHITE, 0))
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
            painter.setPen(QColor(*WHITE, 0))
            painter.setBrush(QGradient(QGradient.Preset.Seashore))
            painter.drawEllipse(
                self.margin_size[0] + (self.board.player_pos[0][1] + 0.25) * self.grid_size,
                self.margin_size[1] + (self.board.player_pos[0][0] + 0.25) * self.grid_size,
                self.grid_size * 0.5,
                self.grid_size * 0.5,
            )

        else:
            painter.setPen(QColor(*WHITE, 0))
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

        painter.setPen(QColor(*WHITE, 0))
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
        light_color = BLUE if self.board.state[12, 0, 0] == 0 else LIGHT_GREEN

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
            grad = QRadialGradient(
                self.margin_size[0] + pos[1] * self.grid_size + self.grid_size / 2,
                self.margin_size[1] + pos[0] * self.grid_size + self.grid_size / 2,
                self.grid_size / 2,
                self.margin_size[0] + pos[1] * self.grid_size + self.grid_size / 2,
                self.margin_size[1] + pos[0] * self.grid_size + self.grid_size / 2,
                self.grid_size / 4
            )

            grad.setColorAt(0, QColor(*light_color, 0))
            grad.setColorAt(1, QColor(*light_color, 180))
            painter.setPen(QColor(*WHITE, 0))
            painter.setBrush(grad)
            painter.drawRoundedRect(
                self.margin_size[0] + pos[1] * self.grid_size + self.padding_size / 2,
                self.margin_size[1] + pos[0] * self.grid_size + self.padding_size / 2,
                self.grid_size - self.padding_size,
                self.grid_size - self.padding_size,
                5,
                5
            )

    def drawFinalTerritory(self, painter: QPainter):
        """
        显示最终领地（游戏结束后）
        :param scr: 屏幕
        :return:
        """
        for pos in self.blue_final_territory:
            painter.fillRect(
                self.margin_size[0] + pos[1] * self.grid_size + self.padding_size / 2,
                self.margin_size[1] + pos[0] * self.grid_size + self.padding_size / 2,
                self.grid_size - self.padding_size,
                self.grid_size - self.padding_size,
                QColor(*LIGHT_BLUE, 100)
            )

        for pos in self.green_final_territory:
            painter.fillRect(
                self.margin_size[0] + pos[1] * self.grid_size + self.padding_size / 2,
                self.margin_size[1] + pos[0] * self.grid_size + self.padding_size / 2,
                self.grid_size - self.padding_size,
                self.grid_size - self.padding_size,
                QColor(*LIGHT_GREEN, 100)
            )

    def drawWall(self, painter: QPainter):
        """
        绘制墙
        :param painter:
        :param scr: 屏幕
        :return:
        """
        for i in range(self.board_len):
            for j in range(self.board_len):
                if self.board.state[6, i, j] == 1:
                    self.drawHorizontalWall(painter, WHITE, i, j)
                if self.board.state[9, i, j] == 1:
                    self.drawVerticalWall(painter, WHITE, i, j)

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
        painter.setPen(QColor(*WHITE, 0))
        painter.setBrush(QColor(*color, 180))
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

        painter.setPen(QColor(*WHITE, 0))
        painter.setBrush(QColor(*color, 180))
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
        :param mouse_pos: 鼠标位置
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

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.mouse_pos = event.x(), event.y()
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.running: return
        action = self.mouse_pos_to_action(event.x(), event.y())
        self.doAction(action)
        self.update()

    def onRestart(self):
        self.board.clear_board()
        self.running = True
        self.active_player_pos_index = 0
        self.blue_final_territory = []
        self.green_final_territory = []
        self.history = []
        self.update()

    def onUndo(self):
        self.board.clear_board()
        self.running = True
        self.active_player_pos_index = 0
        self.blue_final_territory = []
        self.green_final_territory = []
        for action in self.history[:-1]:
            self.board.do_action(action)
        self.history = self.history[:-1]
        self.update()

    def onResign(self):
        ...

    def onSave(self):
        ...

    def createGameOverInfoBar(self, title, content, color):
        w = InfoBar.new(
            icon=FluentIcon.COMPLETED,
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
        w.setCustomBackgroundColor(color, color)

    def doAction(self, action):
        """
        执行动作
        :param action: 动作（0-99整数）
        :return:
        """
        if action not in self.board.available_actions:
            return
        self.board.do_action(action)
        self.history.append(action)

        if self.board.is_game_over_()[0]:
            self.running = False

            self.blue_final_territory = self.board.is_game_over_()[1]
            self.green_final_territory = self.board.is_game_over_()[2]

            self.all_games.append(self.history)

            self.print_result()

        self.active_player_pos_index = 0 if self.board.state[12, 0, 0] == 0 else 3

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
            color = QColor(*BLUE)
        elif blue_score < green_score:
            title += "GREEN WIN!"
            color = QColor(*GREEN)
        else:
            title += "DRAW!"
            color = "white"

        content += f"BLUE:{blue_score}, GREEN:{green_score}"

        self.createGameOverInfoBar(title, content, color)
