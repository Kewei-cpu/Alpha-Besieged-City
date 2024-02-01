# coding:utf-8
import torch
from PySide6.QtCore import QThread, Signal

from alphazero import AlphaZeroMCTS, PolicyValueNet, TerritoryMCTS
from app.common.model_utils import testModel
from app.common.multiprocess_mcts import runMCTS
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
        self.isUseGPU = cfg.get(cfg.useGPU)
        self.device = torch.device('cuda:0' if self.isUseGPU else 'cpu')
        self.model = cfg.get(cfg.modelPath)
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
