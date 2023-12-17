from Algorithms.Greedy.greedy import greedy
from Algorithms.Minimax.minimax import find_best_move
from game_logic import *
import time


def play_greedy_vs_minimax(user_starts=True):
    memo = {}
    print("Minimax = X | Greedy = O")
    boardd = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
              [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
              [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]

    curr = 'O' if user_starts else 'X'

    while check_win(boardd) == 'Y':
        draw_board(boardd)

        if curr == 'X':
            print("Minimax Algorithm is thinking", end='', flush=True)
            time.sleep(1)
            for _ in range(3):
                print('.', end='', flush=True)
                time.sleep(1)
            start_time = time.time()
            move_index = find_best_move(copyboard(boardd), memo)
        else:
            print("Greedy Algorithm is thinking", end='', flush=True)
            time.sleep(1)
            for _ in range(3):
                print('.', end='', flush=True)
                time.sleep(1)
            start_time = time.time()
            move_index = greedy(boardd, curr)
        end_time = time.time()
        move_time = end_time - start_time

        move(move_index, boardd, curr)
        print(f'Move: {move_index}')
        print(f'Time taken for the move: {move_time:.4f} seconds')

        curr = 'O' if curr == 'X' else 'X'

    draw_board(boardd)
    winner = check_win(boardd)
    if winner == 'no one':
        print("It's a tie!")
    else:
        print(f"Player {winner} wins!")


if __name__ == "__main__":
    user_starts = input("Do you want Greedy to go first? (y/n): ").lower() == 'y'
    play_greedy_vs_minimax(user_starts)
