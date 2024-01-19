import torch
from torch.optim import Adam
from torch.optim.lr_scheduler import ExponentialLR
from torch.utils.data import DataLoader
from tqdm import tqdm

from alphazero import PolicyValueNet, ChessBoard
from alphazero.self_play_dataset import SelfPlayDataSet, SelfPlayData
from alphazero.train import PolicyValueLoss
from data_generation import get_data

device = torch.device('cuda:0')
chess_board = ChessBoard(board_len=7)

# 创建数网络
policy_value_net = PolicyValueNet(board_len=7, n_feature_planes=13, policy_output_dim=100, is_use_gpu=True)

# 创建优化器和损失函数
optimizer = Adam(policy_value_net.parameters(), lr=1e-2, weight_decay=1e-4)
criterion = PolicyValueLoss()

# self.lr_scheduler = MultiStepLR(self.optimizer, [1500, 2500], gamma=0.1)
lr_scheduler = ExponentialLR(optimizer, gamma=0.998)  # 0.998 ** 1000 = 0.135

# 创建数据集
dataset = SelfPlayDataSet(board_len=7)

feature_list, pi_list, z_list = get_data('./data/match_history_max_vs_max.json')

dataset.append(
    SelfPlayData(feature_planes_list=feature_list, pi_list=pi_list, z_list=z_list))

policy_value_net.train()

data_loader = DataLoader(dataset, batch_size=100, shuffle=True, drop_last=False)

for epoch in range(100):
    print(f"Epoch {epoch + 1}")
    p_bar = tqdm(enumerate(data_loader, 0), ncols=80)
    for i, data in p_bar:
        p_bar.set_description(f"Batch {i + 1}")

        feature_planes, pi, z = data
        feature_planes, pi, z = feature_planes.to(device), pi.to(device), z.to(device)

        # 前馈
        p_hat, value = policy_value_net(feature_planes)
        # 梯度清零
        optimizer.zero_grad()
        # 计算损失
        loss = criterion(p_hat.float(), pi.float(), value.flatten().float(), z.float())
        # 误差反向传播
        loss.backward()
        # 更新参数
        optimizer.step()
        # 学习率退火
        lr_scheduler.step()

    print(f"Epoch {epoch + 1} Loss: {loss.item():.4f}")
