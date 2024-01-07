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

## Game Rules of _Besieged City_

### Game Board

* The game board is officially a **7x7 grid**, but you can change it to any size you want.
* This game if played with 2 players. **Player Blue** is started on the left top corner, and **Player Green** is started
  on the right bottom corner.

### Move and Place

* **Player Blue** goes first, then two player go in turn. Each turn, a player  **move** his/her pieces, **_AND_** *
  *place** a new wall on the
  board.
* A **step** of move is defined as moving a piece to a neighboring grid (up, down, left, right) that is not occupied by
  another piece or blocked by a wall.
* A legal move can go **0~3** steps, which means the player can stay at the same grid.
* After move, the player **_MUST_** place a wall on the board. The wall can only be placed on one of the **_four sides_
  **
  of the grid that the player move to. Walls cannot be placed on another wall or on the outer edge of the board.

### Win or Lose

* The game ends when two players's pieces are **completely seperated** by walls, which means one player cannot reach the
  other no matter how many steps he/she moves.
* A player's territory is the number of grids that he/she can reach when the game ends. A grid that cannot be reached by
  any player is not counted as any player's territory.
* The player with **_more_** territory wins the game.

## Screenshots

### Starting position

<img width="50%" align="center" src="resources/screenshot/0.png">

### Middle of a game

<img width="50%" align="center" src="resources/screenshot/1.png">
<p></p>
<img width="50%" align="center" src="resources/screenshot/2.png">

### Game over

<img width="50%" align="center" src="resources/screenshot/3.png">

In this case, **Player Blue** wins. (28:21)

## Train model

  ```shell
  conda activate Alpha_Besieged_City 
  python train.py
  ```

## License

Alpha-Besieged-City is licensed under [GPLv3](./LICENSE).

Copyright © 2024 by Kewei-cpu
