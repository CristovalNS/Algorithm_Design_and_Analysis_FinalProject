import time

from random import choice

from Algorithms.Greedy.greedy import greedy
from Algorithms.MCTS.monte_carlo_tree_search import *
from Algorithms.MCTS.monte_carlo_tree_search import MCTS
from Algorithms.Minimax.minimax import find_best_move
from game_logic import check_win, draw_board, copyboard, move


class TicTacToeBoard(Node):
    def __init__(self, tup, turn, winner, terminal, size):
        self.tup = tup
        self.turn = turn
        self.winner = winner
        self.terminal = terminal
        self.size = size


    def find_children(self):
        if self.terminal:
            return set()
        return {
            self.make_move(i) for i, value in enumerate(self.tup) if value is None
        }

    def find_random_child(self):
        if self.terminal:
            return None
        empty_spots = [i for i, value in enumerate(self.tup) if value is None]
        if not empty_spots:
            return None  # No more empty spots, indicating a terminal state
        return self.make_move(choice(empty_spots))

    def reward(self):
        if not self.terminal:
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if self.winner is self.turn:
            raise RuntimeError(f"reward called on unreachable board {self}")
        if self.turn is (not self.winner):
            return 0
        if self.winner is None:
            return 0.5
        raise RuntimeError(f"board has unknown winner type {self.winner}")

    def is_terminal(self):
        return self.terminal

    def make_move(self, index):
        tup = self.tup[:index] + (self.turn,) + self.tup[index + 1:]
        turn = not self.turn
        winner = self._find_winner(tup)
        is_terminal = (winner is not None) or not any(v is None for v in tup)

        self.last_move_index = index # Update last move

        return TicTacToeBoard(tup, turn, winner, is_terminal, self.size)

    def get_last_move_index(self):
        return self.last_move_index

    def to_pretty_string(self):
        to_char = lambda v: ("X" if v is True else ("O" if v is False else " "))
        layers = [self.tup[i:i + self.size ** 2] for i in range(0, len(self.tup), self.size ** 2)]
        return '\n\n'.join([
            f'Layer {i + 1}:\n   {", ".join(map(str, range(1, self.size + 1)))}' + '\n' +
            '\n'.join([
                f'{row + 1}  {"  ".join([to_char(layer[row * self.size + col]) for col in range(self.size)])}' for row
                in range(self.size)
            ]) for i, layer in enumerate(layers)
        ])

    def _winning_combos(self):
        # Horizontal Lines
        yield (0, 1, 2)
        yield (3, 4, 5)
        yield (6, 7, 8)

        yield (9, 10, 11)
        yield (12, 13, 14)
        yield (15, 16, 17)

        yield (18, 19, 20)
        yield (21, 22, 23)
        yield (24, 25, 26)

        # Vertical Lines
        yield (0, 3, 6)
        yield (1, 4, 7)
        yield (2, 5, 8)

        yield (9, 12, 15)
        yield (10, 13, 16)
        yield (11, 14, 17)

        yield (18, 21, 24)
        yield (19, 22, 25)
        yield (20, 23, 26)

        # Depth Lines
        yield (0, 9, 18)
        yield (1, 10, 19)
        yield (2, 11, 20)

        yield (3, 12, 21)
        yield (4, 13, 22)
        yield (5, 14, 23)

        yield (6, 15, 24)
        yield (7, 16, 25)
        yield (8, 17, 26)

        # Diagonal same z layer
        yield (0, 4, 8)  # down-right diagonal layer 1
        yield (2, 4, 6)  # down-left diagonal layer 1

        yield (11, 13, 15) # down-right diagonal layer 2
        yield (9, 13, 17) # down-left diagonal layer 2

        yield (16, 22, 24)  # down-right diagonal layer 3
        yield (18, 22, 26)  # down-left diagonal layer 3

        # Diagonal same y layer
        yield (0, 12, 24)  # down-right diagonal layer 1
        yield (6, 12, 18)  # down-left diagonal layer 1

        yield (1, 13, 25)  # down-right diagonal layer 2
        yield (7, 13, 19)  # down-left diagonal layer 2

        yield (2, 14, 26)  # down-right diagonal layer 3
        yield (8, 14, 20)  # down-left diagonal layer 3

        # Diagonal same x layer
        yield (0, 10, 20)  # down-right diagonal layer 1
        yield (2, 10, 18)  # down-left diagonal layer 1

        yield (3, 13, 25)  # down-right diagonal layer 2
        yield (5, 13, 21)  # down-left diagonal layer 2

        yield (6, 16, 26)  # down-right diagonal layer 3
        yield (8, 16, 24)  # down-left diagonal layer 3

        # Diagonals through the depth
        yield (0, 13, 26)
        yield (2, 13, 24)
        yield (6, 13, 20)
        yield (8, 13, 18)



    def _find_winner(self, tup):
        for combo in self._winning_combos():
            values = [tup[i] for i in combo]
            if all(v is True for v in values):
                return True
            elif all(v is False for v in values):
                return False
        return None

    def __eq__(self, other):
        return (
            isinstance(other, TicTacToeBoard) and
            self.tup == other.tup and
            self.turn == other.turn and
            self.winner == other.winner and
            self.terminal == other.terminal and
            self.size == other.size
        )

    def __hash__(self):
        return hash((self.tup, self.turn, self.winner, self.terminal, self.size))

    def getBoard(self):
        board = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
                 [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
                 [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
        for i in range(27):
            if self.tup[i] is None:
                board[i // 9][i // 3 % 3][i % 3] = '-'
            else:
                board[i // 9][i // 3 % 3][i % 3] = self.tup[i]


def list_to_tictactoe_board(board):
    linear_list = []
    for i in range(27):
        if board[i//9][i//3%3][i%3] == '-':
            linear_list.append(None)
        else:
            linear_list.append(board[i//9][i//3%3][i%3])
    return TicTacToeBoard(tup=tuple(linear_list), turn=True, winner=None, terminal=False, size=size)


def play_three_players():
    print("MCTS = MC | Greedy = GR | Minimax = Mm")
    boardd = [[['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
              [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']],
              [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]]
    players = ['MC', 'GR', 'Mm']  # 'MC' for MCTS, 'GR' for Greedy, 'Mm' for Minimax
    curr_idx = 0

    while check_win(boardd) == 'Y':
        draw_board(boardd)

        curr_player = players[curr_idx]
        print(f"{curr_player}'s turn:")
        start_time = time.time()

        if curr_player == 'X':
            mcts = MCTS()
            for _ in range(1000):
                mcts.do_rollout(list_to_tictactoe_board(boardd))
            move_index = mcts.choose(list_to_tictactoe_board(boardd))
        elif curr_player == 'O':
            move_index = greedy(copyboard(boardd), curr_player)
        else:
            memo = {}
            move_index = find_best_move(copyboard(boardd), memo)

        end_time = time.time()
        move_time = end_time - start_time

        move(move_index, boardd, curr_player)
        print(f'Move: {move_index}')
        print(f'Time taken for the move: {move_time:.4f} seconds')

        curr_idx = (curr_idx + 1) % len(players)

    draw_board(boardd)
    winner = check_win(boardd)
    if winner == 'no one':
        print("It's a tie!")
    else:
        print(f"Player {winner} wins!")


if __name__ == "__main__":
    size = 3  # Set the size here or get it from your logic
    play_three_players()
