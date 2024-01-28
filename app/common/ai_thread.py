# coding:utf-8
import torch
from PySide6.QtCore import QThread, Signal

from alphazero import AlphaZeroMCTS, PolicyValueNet, RolloutMCTS, TerritoryMCTS
from app.common.model_utils import testModel
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
        self.isUseGPU = cfg.get(cfg.useGPU)
        self.device = torch.device('cuda:0' if self.isUseGPU else 'cpu')
        self.model = None
        self.mcts = None
        self.setModel(cfg.get(cfg.modelPath))

    def run(self):
        """ 根据当前局面获取动作 """
        action = self.mcts.get_action(self.chessBoard)
        self.searchComplete.emit(action)

    def setModel(self, model=None, **kwargs):
        """ 设置模型

        model: str
            策略-价值模型路径，如果为 `None`，则使用随机走棋策略
        """

        if model and testModel(model):
            self.model = torch.load(model).to(self.device)  # type:PolicyValueNet
            self.model.set_device(is_use_gpu=self.isUseGPU)
            self.model.eval()
            self.mcts = AlphaZeroMCTS(self.model, self.c_puct, self.n_iters)
        else:
            self.model = None
            self.mcts = TerritoryMCTS(self.c_puct, self.n_iters)
