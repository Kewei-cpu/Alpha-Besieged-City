<p align="center">
  <img width="25%" align="center" src="resources/icon/bluegreen.png" alt="logo">
</p>
  <h1 align="center">
  Alpha Besieged City
</h1>

<p align="center">
  A RL-based AI model of board game "Besieged City"
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Version-v1.0-blue.svg?color=00B16A" alt="Version v1.0"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.10.8-blue.svg?color=00B16A" alt="Python 3.10.8"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PyTorch-2.1.2-blue?color=00B16A" alt="PyTorch 2.1.2"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Pygame-2.5.2-blue?color=00B16A" alt="Pygame 2.5.2"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/OS-Win%2010%20|%20Win%2011-blue?color=00B16A" alt="OS Win10 | Win 11"/>
  </a>
</p>

## Policy-Value Net

* Network structure
    * `ConvBlock` × 1
    * `ResidueBlock` × 4
    * `PolicyHead` × 1
    * `ValueHead` × 1

## Quick start

1. Create virtual environment:

    ```shell
    conda create -n Alpha_Besieged_City python=3.10.8
    conda activate Alpha_Besieged_City
    pip install -r requirements.txt
    ```

2. Install `PyTorch`，refer to the [blog](https://www.cnblogs.com/zhiyiYo/p/15865454.html) for details；


3. Start game:

    ```shell
    conda activate Alpha_Besieged_City 
    python game.py
    ```

## Train model

  ```shell
  conda activate Alpha_Besieged_City 
  python train.py
  ```

## License

Alpha-Besieged-City is licensed under [GPLv3](./LICENSE).

Copyright © 2024 by Kewei-cpu
