import math
import random
import constant as const


class Player:
    def __init__(self):
        self.symbol = None

    def name(self):
        pass

    def set_symbol(self, symbol):
        self.symbol = symbol

    def move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__()
        self.set_symbol(symbol)

    def name(self):
        return 'Human'

    def move(self, game):
        is_correct = False
        cell_number = None
        while not is_correct:
            cell = input('Choose cell number from 0 to 8: ')
            try:
                cell_number = int(cell)
                if cell_number not in game.available_moves():
                    raise ValueError
                is_correct = True
            except ValueError:
                print('Invalid cell number, please try again.')
        return cell_number


class ComputerPlayer(Player):
    def __init__(self, symbol):
        super().__init__()
        self.set_symbol(symbol)

    def name(self):
        return 'Computer'

    def move(self, game):
        if len(game.available_moves()) == 9:
            # For the first move choose the random cell
            cell_number = random.choice(game.available_moves())
        else:
            minmax = self.minimax(game, self.symbol)
            cell_number = minmax['cell']
        return cell_number

    # Implementation of minmax algorithm.
    # {'cell': None, 'score': 0} -> this Set is used to save a state.
    # 'cell' - it's a number of a cell in the square, and 'score' - it's score
    # if we decide to select this cell for the move.
    def minimax(self, state, symbol):
        max_player = self.symbol
        other_player = const.O_SYMBOL if symbol == const.X_SYMBOL else const.X_SYMBOL

        # First check if the previous move is a winner.
        if state.winner == other_player:
            return {'cell': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                            state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'cell': None, 'score': 0}

        if symbol == max_player:
            # Each score should maximize.
            best = {'cell': None, 'score': -math.inf}
        else:
            # Each score should minimize.
            best = {'cell': None, 'score': math.inf}
        for possible_move in state.available_moves():
            state.make_move(possible_move, symbol)

            # After the move let's simulate a game.
            sim_score = self.minimax(state, other_player)

            # Undo the move.
            state.board[possible_move] = ' '
            state.winner = None
            # This represents the move optimal next move.
            sim_score['cell'] = possible_move

            if symbol == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best
