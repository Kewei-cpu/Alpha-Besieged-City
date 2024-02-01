# coding:utf-8
from PySide6.QtCore import QThread, Signal

from alphazero import TerritoryMCTS
from app.config import *

from multiprocessing import Pool


class AIThread(QThread):
    """ AI """

    searchComplete = Signal(int)

    def __init__(self, chessBoard, parent=None):
        """
        Parameters
        ----------
        board: ChessBoard
            棋盘

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
        p = Pool(1)
        action = p.apply_async(self.mcts.get_action, (self.chessBoard,)).get()
        self.searchComplete.emit(action)
