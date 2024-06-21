from collections import namedtuple, deque
import random
from .painter import PaintBoard


Pawn = namedtuple("Pawn", "index colour id")


class Player():
    def __init__(self, colour, name=None, choose_pawn_delegate=None):
        self.colour = colour
        self.choose_pawn_delegate = choose_pawn_delegate
        self.name = name
        if self.name is None and self.choose_pawn_delegate is None:
            self.name = "computer"
        self.finished = False
        self.pawns = [Pawn(i, colour, colour[0].upper() + str(i)) for i in range(1, 5)]

    def __str__(self):
        return "{}({})".format(self.name, self.colour)

    def choose_pawn(self, pawns):
        if len(pawns) == 1:
            index = 0
        elif len(pawns) > 1:
            if self.choose_pawn_delegate is None:
                index = random.randint(0, len(pawns) - 1)
            else:
                index = self.choose_pawn_delegate(pawns)
        return index

class Board():
    BOARD_SIZE = 56
    BOARD_COLOUR_SIZE = 7
    COLOUR_ORDER = ['yellow', 'blue', 'red', 'green']
    COLOUR_DISTANCE = 14

    def __init__(self):
        Board.COLOUR_START = {
            colour: 1 + index * Board.COLOUR_DISTANCE for
            index, colour in enumerate(Board.COLOUR_ORDER)}
        Board.COLOUR_END = {
            colour: index * Board.COLOUR_DISTANCE
            for index, colour in enumerate(Board.COLOUR_ORDER)}
        Board.COLOUR_END['yellow'] = Board.BOARD_SIZE
        self.pawns_possiotion = {}
        self.painter = PaintBoard()
        self.board_pool_position = (0, 0)

    def set_pawn(self, pawn, position):
        self.pawns_possiotion[pawn] = position

    def put_pawn_on_board_pool(self, pawn):
        self.set_pawn(pawn, self.board_pool_position)

    def is_pawn_on_board_pool(self, pawn):
        return self.pawns_possiotion[pawn] == self.board_pool_position

    def put_pawn_on_starting_square(self, pawn):
        start = Board.COLOUR_START[pawn.colour.lower()]
        position = (start, 0)
        self.set_pawn(pawn, position)

    def can_pawn_move(self, pawn, rolled_value):
        common_poss, private_poss = self.pawns_possiotion[pawn]
        if private_poss + rolled_value > self.BOARD_COLOUR_SIZE:
            return False
        return True