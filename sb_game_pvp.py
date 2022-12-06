from SB_game import IGame
from SB_board import GameBoard
from SB_board import pvp_result
from SB_cell import CellState
from SB_helpers import sb_strings


class PVP_game(IGame):

    def __init__(self):
        self.finished = False
        self.gameOver = False

        self.myBoard = GameBoard()
        self.hisBoard = GameBoard()
        self.firstset = 0
        self.motion = IGame.MOTION_NONE

        self.draw_text(sb_strings.letsbegin)

    def iteration(self):
        if self.firstset >= GameBoard._shipsCountAll:
                if self.myBoard.AllShipsDestroyed():
                    self.lose()
                    self.gameOver = True
                if self.hisBoard.AllShipsDestroyed():
                    self.win()
                    self.gameOver = True

    def attack_him(cls, nx, ny):
        if cls.hisBoard.getCell(nx, ny) == CellState.HitDeck \
                or cls.hisBoard.getCell(nx, ny) == CellState.Miss:
            return True
        return cls.hisBoard.Shoot(nx, ny)

    def pole_event(self, x, y, sender):
        if self.checkWin():
            return
        if self.firstset < GameBoard._shipsCountAll:
            self.prepare(x, y, sender)
            return
        elif self.getMotion() == IGame.MOTION_MY:
            if sender == self.SENDER_HISBOARD:
                if not self.attack_him(x, y):
                    self.draw_text(sb_strings.motion2)
                    self.setMotion(IGame.MOTION_HIS)
                    return
        elif self.getMotion() == IGame.MOTION_HIS:
            if sender == self.SENDER_MYBOARD:
                if not self.attack_me(x, y):
                    self.draw_text(sb_strings.motion1)
                    self.setMotion(IGame.MOTION_MY)
                    return

    def position_result_handler(self, result):
        if result == pvp_result.ok:
            self.firstset += 1
            self.draw_text('')  #self.screen.fill(sb_colors.gray)
        elif result == pvp_result.incorrect:
            self.draw_text(sb_strings.pr_incorrect)
        elif result == pvp_result.out_of_pole:
            self.draw_text(sb_strings.pr_out)
        elif result == pvp_result.overflow:
            self.draw_text(sb_strings.pr_ovf)
        elif result == pvp_result.cant_pos:
            self.draw_text(sb_strings.pr_cant)

    def prepare(self, msx, msy, sender): #FIXME rename
        if self.firstset < GameBoard._shipsCount:
            self.myBoard.unhide()
            if sender == self.SENDER_MYBOARD:
                self.position_result_handler(
                    self.myBoard.PvP(msx, msy, self.rank,
                                        self.hori, self.firstset))

        if self.firstset == GameBoard._shipsCount:
            self.myBoard.hide()
            self.rank = 0
            self.hori = True
            self.draw_text(sb_strings.prepare10)
            self.firstset += 1
            return

        if self.firstset < GameBoard._shipsCountAll \
                and self.firstset >= GameBoard._shipsCount:
            self.hisBoard.unhide()
            if sender == self.SENDER_HISBOARD:
                self.position_result_handler(
                    self.hisBoard.PvP(msx, msy, self.rank,
                                    self.hori, self.firstset))

        if self.firstset >= GameBoard._shipsCountAll:
            self.hisBoard.hide()
            self.draw_text(sb_strings.prepare_done1)
            self.setMotion(IGame.MOTION_MY)

    def win(cls):
        cls.gameOver = True
        cls.myBoard.unhide()
        cls.hisBoard.unhide()
        cls.draw_text(sb_strings.win)

    def lose(cls):
        cls.gameOver = True
        cls.myBoard.unhide()
        cls.hisBoard.unhide()
        cls.draw_text(sb_strings.lose)

    def checkWin(cls):
            return cls.myBoard.AllShipsDestroyed() \
                or cls.myBoard.AllShipsDestroyed()

if __name__ == "__main__":
    print("This module is not for direct call!")
