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

    def move_pawn(self, pawn, rolled_value):
        common_poss, private_poss = self.pawns_possiotion[pawn]
        end = self.COLOUR_END[pawn.colour.lower()]
        if private_poss > 0:
            private_poss += rolled_value
        elif common_poss <= end and common_poss + rolled_value > end:
            # pawn is entering in own squares
            private_poss += rolled_value - (end - common_poss)
            common_poss = end
        else:
            # pawn will be still in common square
            common_poss += rolled_value
            if common_poss > self.BOARD_SIZE:
                common_poss = common_poss - self.BOARD_SIZE
        position = common_poss, private_poss
        self.set_pawn(pawn, position)

        def does_pawn_reach_end(self, pawn):
            common_poss, private_poss = self.pawns_possiotion[pawn]
            if private_poss == self.BOARD_COLOUR_SIZE:
                return True
            return False

        def get_pawns_on_same_postion(self, pawn):
            position = self.pawns_possiotion[pawn]
            return [curr_pawn for curr_pawn, curr_postion in
                    self.pawns_possiotion.items()
                    if position == curr_postion]

        def paint_board(self):
            positions = {}
            for pawn, position in self.pawns_possiotion.items():
                common, private = position
                if not private == Board.BOARD_COLOUR_SIZE:
                    positions.setdefault(position, []).append(pawn)
            return self.painter.paint(positions)

    class Die():
        MIN = 1
        MAX = 6

        @staticmethod
        def throw():
            return random.randint(Die.MIN, Die.MAX)

    class Game():
        def __init__(self):
            self.players = deque()
            self.standing = []
            self.board = Board()
            self.finished = False
            self.rolled_value = None
            self.curr_player = None
            self.allowed_pawns = []
            self.picked_pawn = None
            self.index = None
            self.jog_pawns = []

        def add_palyer(self, player):
            self.players.append(player)
            for pawn in player.pawns:
                self.board.put_pawn_on_board_pool(pawn)

        def get_available_colours(self):
            used = [player.colour for player in self.players]
            available = set(self.board.COLOUR_ORDER) - set(used)
            return sorted(available)

