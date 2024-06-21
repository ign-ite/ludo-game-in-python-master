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