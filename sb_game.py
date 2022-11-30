#FIXME game parent class

class Game:
    def mainloop(self):
        ...
    def attack_him(cls, nx, ny):
        ...
    def attack_me(cls, nx, ny):
        ...
    def pole_event(cls, y, x, sender):
        ...
    def prepare(cls, msx, msy, sender):
        ...
    HOD_NONE = 0
    HOD_MY = 1
    HOD_HIS = 2
    hod = HOD_NONE

    def setHod(cls, ipt):
        ...# Game.hod = ipt

    def getHod(cls):
        ...# return Game.hod

    def checkWin(cls):
        ...# return Game.myBoard.AllShipsDestroyed() or Game.myBoard.AllShipsDestroyed()

    def win(cls):
        ...

    def lose(cls):
        ...

    def draw_cells(cls, unhide=True):
        ...

class Online_game(Game):
    ...

class Pvp_game(Game):
    ...