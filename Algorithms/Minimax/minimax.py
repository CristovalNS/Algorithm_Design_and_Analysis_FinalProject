def rotateZ(board):
    board2 = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
         [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                board2[i][j][k] = board[i][k][((j-1)*-1)+1]
    return board2

def rotateX(board):
    board2 = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
         [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                board2[i][j][k] = board[((j-1)*-1)+1][i][k]
    return board2


def flip(board):
    board[0], board[2] = board[2], board[0]

def spin(board):
    board2 = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
              [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                board2[i][j][k] = board[k][i][j]
    return board2

board = [[['a', 'b', '-'], ['c', '-', '-'], ['-', '-', '-']], [['d', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
         [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]



def listdown(board):
    board2 = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
              [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                board2[i][j][k] = board[i][j][k]
    listt = []
    for i in range(2):
        flip(board2)
        board2 = rotateX(board2)
        for j in range(3):
            board2 = spin(board2)
            if str(board2) not in listt:
                listt.append(str(board2))
            for j in range(4):
                board2 = rotateZ(board2)
                if str(board2) not in listt:
                    listt.append(str(board2))
            rotateX(board2)
            for j in range(4):
                board2 = rotateZ(board2)
                if str(board2) not in listt:
                    listt.append(str(board2))
            for j in range(3):
                if str(board2) not in listt:
                    listt.append(str(board2))
    return listt

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


def minimax(board, maximizing_player, memo, alpha, beta, depth=0):
    # Check if the current state has been memoized
    board_key = str(board)
    if board_key in memo:
        return memo[board_key]

    winner = check_win(board)
    if winner == 'X':
        for k in listdown(board):
            memo[k] = -1  # X (maximizing player) wins
        return -1
    elif winner == 'O':
        for k in listdown(board):
            memo[k] = 1   # O (minimizing player) wins
        return 1
    elif winner == 'no one':
        for k in listdown(board):
            memo[k] = 0   # It's a draw
        return 0


    if maximizing_player:
        for i in range(27):
            if board[i // 9][i // 3 % 3][i % 3] == '-':
                board[i // 9][i // 3 % 3][i % 3] = 'O'
                if check_win(board) == 'O':
                    for k in listdown(board):
                        memo[k] = 1  # O (minimizing player) wins
                    board[i // 9][i // 3 % 3][i % 3] = '-'  # Undo the move
                    return 1
                board[i // 9][i // 3 % 3][i % 3] = '-'  # Undo the move
        max_eval = float('-inf')
        for i in range(27):
            if board[i // 9][i // 3 % 3][i % 3] == '-':
                board[i // 9][i // 3 % 3][i % 3] = 'O'
                evaluated = minimax(board, False, memo, alpha, beta, depth + 1)
                board[i // 9][i // 3 % 3][i % 3] = '-'  # Undo the move
                max_eval = max(max_eval, evaluated)
                alpha = max(alpha, evaluated)
                if beta <= alpha:
                    break  # Prune remaining branches
        for k in listdown(board):
            memo[k] = max_eval
        return max_eval
    else:
        for i in range(27):
            if board[i // 9][i // 3 % 3][i % 3] == '-':
                board[i // 9][i // 3 % 3][i % 3] = 'X'
                if check_win(board) == 'X':
                    for k in listdown(board):
                        memo[k] = -1  # X (maximizing player) wins
                    board[i // 9][i // 3 % 3][i % 3] = '-'  # Undo the move
                    return -1
                board[i // 9][i // 3 % 3][i % 3] = '-'  # Undo the move
        min_eval = float('inf')
        for i in range(27):
            if board[i // 9][i // 3 % 3][i % 3] == '-':
                board[i // 9][i // 3 % 3][i % 3] = 'X'
                evaluated = minimax(board, True, memo, alpha, beta, depth + 1)
                board[i // 9][i // 3 % 3][i % 3] = '-'  # Undo the move
                min_eval = min(min_eval, evaluated)
                beta = min(beta, evaluated)
                if beta <= alpha:
                    break  # Prune remaining branches
        for k in listdown(board):
            memo[k] = min_eval
        return min_eval

def find_best_move(board, memo):
    best_val = float('-inf')
    best_move = -1
    alpha = float('-inf')
    beta = float('inf')

    for i in range(27):
        if board[i // 9][i // 3 % 3][i % 3] == '-':
            board[i // 9][i // 3 % 3][i % 3] = 'O'
            if check_win(board) == 'O':
                board[i // 9][i // 3 % 3][i % 3] = '-'
                return i
            board[i // 9][i // 3 % 3][i % 3] = '-'
    for i in range(27):
        if board[i // 9][i // 3 % 3][i % 3] == '-':
            board[i // 9][i // 3 % 3][i % 3] = 'X'
            if check_win(board) == 'X':
                board[i // 9][i // 3 % 3][i % 3] = '-'
                return i
            board[i // 9][i // 3 % 3][i % 3] = '-'

    for i in range(27):
        if board[i // 9][i // 3 % 3][i % 3] == '-':
            board[i // 9][i // 3 % 3][i % 3] = 'O'
            move_val = minimax(board, False, memo, alpha, beta)
            board[i // 9][i // 3 % 3][i % 3] = '-'  # Undo the move
            # print(i, move_val)
            if move_val > best_val:
                best_val = move_val
                best_move = i

            alpha = max(alpha, move_val)

    return best_move


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


# memo = {}
# boardd = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
#           [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
#           [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
# curr = 'X'
#
# while check_win(boardd) == 'Y':
#     if curr == 'X':
#         draw_board(boardd)
#         while move(int(input("Enter 0-26: ")), boardd, curr) == -1:
#             print('Invalid move. Try again.')
#         curr = 'O'
#     else:
#         move(find_best_move(copyboard(boardd), memo), boardd, curr)
#         curr = 'X'
#
# draw_board(boardd)
# winner = check_win(boardd)
# if winner == 'no one':
#     print("It's a tie!")
# else:
#     print(f"Player {winner} wins!")