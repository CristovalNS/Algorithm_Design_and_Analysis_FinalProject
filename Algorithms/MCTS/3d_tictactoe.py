import time
from random import choice
from monte_carlo_tree_search import MCTS, Node

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
        tup = self.tup[:index] + (self.turn,) + self.tup[index + 1 :]
        turn = not self.turn
        winner = self._find_winner(tup)
        is_terminal = (winner is not None) or not any(v is None for v in tup)
        return TicTacToeBoard(tup, turn, winner, is_terminal, self.size)

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

        # Diagonal same layer
        yield (0, 4, 8)  # down-right diagonal layer 1
        yield (2, 4, 6)  # down-left diagonal layer 1

        yield (11, 13, 15) # down-right diagonal layer 2
        yield (9, 13, 17) # down-left diagonal layer 2

        yield (16, 22, 24)  # down-right diagonal layer 2
        yield (18, 22, 26)  # down-left diagonal layer 2

        # Straight down
        yield (0, 9, 18)
        yield (1, 10, 19)
        yield (2, 11, 20)
        yield (3, 12, 21)
        yield (4, 13, 22)
        yield (5, 14, 23)
        yield (6, 15, 24)
        yield (7, 16, 25)
        yield (8, 17, 26)

        # Diagonals through the depth
        yield (0, 13, 26)
        yield (2, 13, 24)
        yield (6, 13, 20)
        yield (8, 13, 18)

        # TODO: Still needs to add more win combos


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



def new_tic_tac_toe_board(size):
    return TicTacToeBoard(tup=(None,) * size**3, turn=True, winner=None, terminal=False, size=size)


def play_game():
    size = 3
    tree = MCTS()

    # Ask the player if they want to go first
    player_first = input("Do you want to go first? (y/n): ").lower() == 'y'

    # Create the initial board
    board = new_tic_tac_toe_board(size)

    print(board.to_pretty_string())

    while True:
        if player_first:
            move = input("Player's turn. Enter move as layer,row,col (e.g., 1,2,3): ")
            layer, row, col = map(int, move.split(","))
            index = size * size * (layer - 1) + size * (row - 1) + (col - 1)

            if board.tup[index] is not None:
                raise RuntimeError("Invalid move")

            print(f"Selected index: {index}")  # Print the index here

            board = board.make_move(index)
            print(board.to_pretty_string())

            if board.terminal:
                break

        print("AI is thinking", end='', flush=True)
        for _ in range(3):  # Adjust the number of dots as needed
            time.sleep(0.5)  # Adjust the delay between dots as needed
            print('.', end='', flush=True)

        print()

        for _ in range(750):
            tree.do_rollout(board)

        board = tree.choose(board)
        print(board.to_pretty_string())

        if board.terminal:
            break

        if not player_first:
            move = input("Player's turn. Enter move as layer,row,col (e.g., 1,2,3): ")
            layer, row, col = map(int, move.split(","))
            index = size * size * (layer - 1) + size * (row - 1) + (col - 1)

            if board.tup[index] is not None:
                raise RuntimeError("Invalid move")

            print(f"Selected index: {index}")  # Print the index here

            board = board.make_move(index)
            print(board.to_pretty_string())

            if board.terminal:
                break

    if board.winner is not None:
        print(f"Player {'X' if board.winner else 'O'} wins!")
        # Print the winning indices
        for combo in board._winning_combos():
            values = [board.tup[i] for i in combo]
            if all(v is True for v in values) or all(v is False for v in values):
                print(f"Winning indices: {combo}")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()



