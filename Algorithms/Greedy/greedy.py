import random
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


def greedy(board, curr):
    if curr == 'X':
        opp = 'O'
    else:
        opp = 'X'
    possible = []
    for i in range(27):
        possible.append(i)
        if board[i // 9][i // 3 % 3][i % 3] == '-':
            board[i // 9][i // 3 % 3][i % 3] = curr
            if check_win(board) == curr:
                board[i // 9][i // 3 % 3][i % 3] = '-'
                return i
            board[i // 9][i // 3 % 3][i % 3] = '-'
    for i in range(27):
        if board[i // 9][i // 3 % 3][i % 3] == '-':
            board[i // 9][i // 3 % 3][i % 3] = opp
            if check_win(board) == opp:
                board[i // 9][i // 3 % 3][i % 3] = '-'
                return i
            board[i // 9][i // 3 % 3][i % 3] = '-'
    return random.choice(possible)


def move(i, board, curr):
    if board[i//9][i//3%3][i%3] != '-':
        return -1
    board[i // 9][i // 3 % 3][i % 3] = curr


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


# def main():
#     boardd = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
#               [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
#               [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
#     curr = 'X'
#
#     while check_win(boardd) == 'Y':
#         if curr == 'X':
#             draw_board(boardd)
#             move_input = int(input("Enter 0-26: "))
#             while move(move_input, boardd, curr) == -1:
#                 print('Invalid move. Try again.')
#                 move_input = int(input("Enter 0-26: "))
#             curr = 'O'
#         else:
#             move(greedy(boardd, curr), boardd, curr)
#             curr = 'X'
#
#         winner = check_win(boardd)
#         if winner != 'Y':
#             draw_board(boardd)
#             if winner == 'no one':
#                 print("It's a tie!")
#             else:
#                 print(f"Player {winner} wins!")
#             break
#
#
# if __name__ == "__main__":
#     main()