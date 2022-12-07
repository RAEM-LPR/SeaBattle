from SB_game import IGame
from SB_game import SB_motion
from SB_board import GameBoard
from SB_board import Ship_set_result
from SB_cell import CellState
from SB_helpers import SB_strings


class PVP_game(IGame):

    def __init__(self):
        self.finished = False
        self.gameOver = False

        self.myBoard = GameBoard(self.SENDER_MYBOARD)
        self.hisBoard = GameBoard(self.SENDER_HISBOARD)
        self.firstset = 0
        self.motion = SB_motion.NONE

        self.draw_text(SB_strings.letsbegin)

    def iteration(self):
        if self.firstset >= GameBoard._shipsCountAll:
            if self.myBoard.AllShipsDestroyed():
                self.lose()
                self.gameOver = True
            if self.hisBoard.AllShipsDestroyed():
                self.win()
                self.gameOver = True

    def attack_him(cls, nx, ny):
        if cls.hisBoard.getCell(nx, ny) == CellState.HIT_DECK \
                or cls.hisBoard.getCell(nx, ny) == CellState.MISS:
            return True
        return cls.hisBoard.Shoot(nx, ny)

    def pole_event(self, x, y, sender):
        if self.checkWin():
            return
        if self.firstset < GameBoard._shipsCountAll:
            self.set_ships(x, y, sender)
            return
        elif self.getMotion() == SB_motion.MY:
            if sender == self.SENDER_HISBOARD:
                if not self.attack_him(x, y):
                    self.draw_text(SB_strings.motion2)
                    self.setMotion(SB_motion.HIS)
                    return
        elif self.getMotion() == SB_motion.HIS:
            if sender == self.SENDER_MYBOARD:
                if not self.attack_me(x, y):
                    self.draw_text(SB_strings.motion1)
                    self.setMotion(SB_motion.MY)
                    return

    def position_result_handler(self, result):
        if result == Ship_set_result.OK:
            self.firstset += 1
            self.draw_text('')
        elif result == Ship_set_result.INCORRECT:
            self.draw_text(SB_strings.pr_incorrect)
        elif result == Ship_set_result.OUT_OF_POLE:
            self.draw_text(SB_strings.pr_out)
        elif result == Ship_set_result.OVERCOUNT:
            self.draw_text(SB_strings.pr_ovf)
        elif result == Ship_set_result.CANT_SET:
            self.draw_text(SB_strings.pr_cant)

    def set_ships(self, msx, msy, sender):
        if self.firstset < GameBoard._shipsCount:
            self.myBoard.unhide()
            if sender == self.SENDER_MYBOARD:
                self.position_result_handler(
                    self.myBoard.try_set_ship(
                        msx, msy, self.ship_rank,
                        self.ship_isHorisontal, self.firstset))

        if self.firstset == GameBoard._shipsCount:
            self.myBoard.hide()
            self.ship_rank = 0
            self.ship_isHorisontal = True
            self.draw_text(SB_strings.prepare10)
            self.firstset += 1
            return

        if self.firstset < GameBoard._shipsCountAll \
                and self.firstset >= GameBoard._shipsCount:
            self.hisBoard.unhide()
            if sender == self.SENDER_HISBOARD:
                self.position_result_handler(
                    self.hisBoard.try_set_ship(
                        msx, msy, self.ship_rank,
                        self.ship_isHorisontal, self.firstset))

        if self.firstset >= GameBoard._shipsCountAll:
            self.hisBoard.hide()
            self.draw_text(SB_strings.prepare_done1)
            self.setMotion(SB_motion.MY)

    def win(cls):
        cls.gameOver = True
        cls.myBoard.unhide()
        cls.hisBoard.unhide()
        cls.draw_text(SB_strings.win)

    def lose(cls):
        cls.gameOver = True
        cls.myBoard.unhide()
        cls.hisBoard.unhide()
        cls.draw_text(SB_strings.lose)

    def checkWin(cls):
        return cls.myBoard.AllShipsDestroyed() \
            or cls.myBoard.AllShipsDestroyed()


if __name__ == "__main__":
    print("This module is not for direct call!")
