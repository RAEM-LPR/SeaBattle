from sb_cell import CellState

class sb_hod: #FIXME
    NONE = 0
    MY = 1
    HIS = 2
    MY_WAIT = 3

class IGame:
    myBoard = None
    hisBoard = None
    
    gameOver = False

    rank = 0
    hori = True

    HOD_NONE = 0
    HOD_MY = 1
    HOD_HIS = 2
    hod = HOD_NONE

    draw_text_buffer = None

    SENDER_MYBOARD = 1 #FIXME use it
    SENDER_HISBOARD = 2

    def __init__(self):
        ...

    def iteration(self):
        ...

    def attack_him(cls, nx, ny):
        ...

    def attack_me(cls, nx, ny):
        if cls.myBoard.getCell(nx, ny) == CellState.HitDeck \
                or cls.myBoard.getCell(nx, ny) == CellState.Miss:
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
        ...  # return Game.myBoard.AllShipsDestroyed() or Game.myBoard.AllShipsDestroyed()

    def win(cls):
        print('win')
        cls.gameOver = True #FIXME

    def lose(cls):
        print('lose')
        cls.gameOver = True #FIXME

    def draw_text(cls, str):
        cls.draw_text_buffer = str


if __name__ == "__main__":
    print("This module is not for direct call!")
