import pygame

from sb_board import GameBoard
from sb_board import GameTable
from sb_board import pvp_result
from sb_cell import CellState
from sb_helpers import sb_pair
from sb_helpers import sb_colors
from sb_helpers import sb_strings
from sb_link import sb_link
from sb_ship import ShipState


class IGame:
    myBoard = None
    hisBoard = None

    rank = 0
    hori = 0

    HOD_NONE = 0
    HOD_MY = 1
    HOD_HIS = 2
    hod = HOD_NONE

    draw_text_buffer = None

    def __init__(self):
        ...

    def iteration(self):
        ...

    def attack_him(cls, nx, ny):
        ...
    
    def attack_me(cls, nx, ny):
        if cls.myBoard.getCell(ny, nx) == CellState.HitDeck \
                or cls.myBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.myBoard.Shoot(nx, ny)


    def pole_event(cls, y, x, sender):
        ...

    def prepare(cls, msx, msy, sender):
        ...

    def setHod(cls, ipt):
        cls.hod = ipt

    def getHod(cls):
        return cls.hod

    def checkWin(cls):
        ...# return Game.myBoard.AllShipsDestroyed() or Game.myBoard.AllShipsDestroyed()

    def win(cls):
        ...

    def lose(cls):
        ...

    def draw_text(cls, str):
        cls.draw_text_buffer = str


if __name__ == "__main__":
    print("This module is not for direct call!")
