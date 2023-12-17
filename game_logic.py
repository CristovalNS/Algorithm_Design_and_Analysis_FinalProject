def check_win(board):
    # 3D diagonals
    for i in range(4):
        if board[1][1][1] == board[0][(i % 2) * 2][(i // 2) * 2] == board[2][((i % 2) - 1) * -2][((i // 2) - 1) * -2] != '-':
            return board[1][1][1]

    # 2D diagonals
    for i in range(3):
        if board[i][0][2] == board[i][1][1] == board[i][2][0] != '-':
            return board[i][1][1]
        if board[i][0][0] == board[i][1][1] == board[i][2][2] != '-':
            return board[i][1][1]
        if board[0][i][2] == board[1][i][1] == board[2][i][0] != '-':
            return board[1][i][1]
        if board[0][i][0] == board[1][i][1] == board[2][i][2] != '-':
            return board[1][i][1]
        if board[0][2][i] == board[1][1][i] == board[2][0][i] != '-':
            return board[1][1][i]
        if board[0][0][i] == board[1][1][i] == board[2][2][i] != '-':
            return board[1][1][i]

    # Straights
    for i in range(3):
        for j in range(3):
            if board[i][j][0] == board[i][j][1] == board[i][j][2] != '-':
                return board[i][j][0]
            if board[i][0][j] == board[i][1][j] == board[i][2][j] != '-':
                return board[i][0][j]
            if board[0][i][j] == board[1][i][j] == board[2][i][j] != '-':
                return board[0][i][j]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                if board[i][j][k] == '-':
                    return 'Y'
    return "no one"


def draw_board(board):
    toPrint = board.copy()
    for i in range(3):
        print("   ".join([str(toPrint[j][i]) for j in range(3)]))


def copyboard(board):
    toReturn = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
         [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                toReturn[i][j][k] = board[i][j][k]
    return toReturn


def move(i, board, curr):
    if board[i // 9][i // 3 % 3][i % 3] != '-':
        return -1
    board[i // 9][i // 3 % 3][i % 3] = curr


def unravel_index(index, shape):
    size = 1
    coords = []
    for dim in reversed(shape):
        size *= dim
        coords.append(index % dim)
        index //= dim
    return tuple(reversed(coords))


def print_board(board):
    for layer in board:
        for row in layer:
            print(" ".join(row))
            print()
        print("---" * len(layer))
    print()
