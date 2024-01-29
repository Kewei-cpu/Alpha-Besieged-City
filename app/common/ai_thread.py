# coding:utf-8
from PySide6.QtCore import QThread, Signal

from alphazero import TerritoryMCTS
from app.config import *


class AIThread(QThread):
    """ AI """

    searchComplete = Signal(int)

    def __init__(self, chessBoard, parent=None):
        """
        Parameters
        ----------
        board: ChessBoard
            棋盘

        model: str
            模型路径

        c_puct: float
            探索常数

        n_iters: int
            蒙特卡洛树搜索次数

        is_use_gpu: bool
            是否使用 GPU

        parent:
            父级
        """
        super().__init__(parent=parent)
        self.chessBoard = chessBoard
        self.c_puct = cfg.get(cfg.cPuct)
        self.n_iters = cfg.get(cfg.numIter)
        self.mcts = TerritoryMCTS(self.c_puct, self.n_iters)

    def run(self):
        """ 根据当前局面获取动作 """
        action = self.mcts.get_action(self.chessBoard)
        self.searchComplete.emit(action)
