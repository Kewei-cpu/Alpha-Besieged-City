from alphazero import ChessBoard

num_to_place = {
    0: 'U',
    1: 'L',
    2: 'D',
    3: 'R'
}

place_to_num = {
    'U': 0,
    'L': 1,
    'D': 2,
    'R': 3
}


def convertMoveToNotation(move_list, board_len=7):
    notation_list = []

    blue_pos = (0, 0)
    green_pos = (board_len - 1, board_len - 1)

    for i, move in enumerate(move_list):
        go = move // 4
        place = move % 4
        rel_pos = ChessBoard.action_to_pos[go]

        if i % 2 == 0:
            blue_pos = (blue_pos[0] + rel_pos[0], blue_pos[1] + rel_pos[1])

            notation = ""
            notation += chr(blue_pos[1] + 97)
            notation += str(board_len - blue_pos[0])
            notation += num_to_place[place]

        else:
            green_pos = (green_pos[0] + rel_pos[0], green_pos[1] + rel_pos[1])

            notation = ""
            notation += chr(green_pos[1] + 97)
            notation += str(board_len - green_pos[0])
            notation += num_to_place[place]

        notation_list.append(notation)

    return notation_list


if __name__ == '__main__':
    print(convertMoveToNotation([83, 18, 81, 28]))
