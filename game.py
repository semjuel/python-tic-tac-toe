import math
from player import Player, HumanPlayer, ComputerPlayer
import constant as const


class Game:
    def __init__(self, x: Player, o: Player):
        self.board = self.init_board()
        self.winner = None
        self.current_player = self.player_x = x
        self.player_o = o

    @staticmethod
    def init_board():
        return [' ' for _ in range(9)]

    def print_board(self):
        for row in [self.board[i*3:(i+1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_with_numbers():
        board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in board:
            print(' | '.join(row))

    def make_move(self, cell_number, symbol):
        if self.board[cell_number] == ' ':
            self.board[cell_number] = symbol
            if self.is_winner(cell_number, symbol):
                self.winner = symbol
            return True
        return False

    # This method checks for a winner in the game.
    # Returns True when current user is a winner.
    def is_winner(self, cell_number, symbol):
        # Check the row
        row_ind = math.floor(cell_number / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == symbol for s in row]):
            return True
        col_ind = cell_number % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == symbol for s in column]):
            return True
        if cell_number % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == symbol for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == symbol for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

    def switch_player(self):
        if self.current_player.symbol == const.X_SYMBOL:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x

    def play(self):
        # First print board with numbers
        self.print_board_with_numbers()

        while self.empty_squares():
            print('It\'s a ' + self.current_player.name() + ' move:')
            # Get cell number that player choosen for his move
            cell = self.current_player.move(self)

            if self.make_move(cell, self.current_player.symbol):
                self.print_board()

            if self.winner:
                print(self.current_player.name() + ' is a winner!')
                # Stop the while loop
                return

            # Switch player
            self.switch_player()

    print("It's a tie.")


if __name__ == '__main__':
    # Computer starts first.
    x_player = ComputerPlayer(const.X_SYMBOL)
    o_player = HumanPlayer(const.O_SYMBOL)
    g = Game(x_player, o_player)
    g.play()
