from sb_game import IGame
from sb_board import GameBoard
from sb_board import pvp_result
from sb_cell import CellState
from sb_helpers import sb_strings


class Pvp_game(IGame):

    def __init__(self):
        self.finished = False
        self.gameOver = False

        self.myBoard = GameBoard()
        self.hisBoard = GameBoard()
        self.firstset = 0
        self.hod = IGame.HOD_NONE

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
        if cls.hisBoard.getCell(ny, nx) == CellState.HitDeck \
                or cls.hisBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.hisBoard.Shoot(nx, ny)

    def pole_event(self, y, x, sender):
        if self.checkWin():
            return True
        if self.firstset < GameBoard._shipsCountAll:
            self.prepare(x, y, sender)
            return True
        elif self.getHod() == IGame.HOD_MY:
            if sender == 2:
                if not self.attack_him(x, y):
                    self.draw_text(sb_strings.hod2)
                    self.setHod(IGame.HOD_HIS)
                    return True
            else:
                return False
        elif self.getHod() == IGame.HOD_HIS:
            if sender == 1:
                if not self.attack_me(x, y):
                    self.draw_text(sb_strings.hod1)
                    self.setHod(IGame.HOD_MY)
                    return True
            else:
                return False
        if self.checkWin():
            return True
        return False

    def position_result_handler(self, result):
        if result == pvp_result.ok:
            self.firstset += 1
            self.draw_text('')#self.screen.fill(sb_colors.gray)
        elif result == pvp_result.incorrect:
            self.draw_text(sb_strings.pr_incorrect)
        elif result == pvp_result.out_of_pole:
            self.draw_text(sb_strings.pr_out)
        elif result == pvp_result.overflow:
            self.draw_text(sb_strings.pr_ovf)
        elif result == pvp_result.cant_pos:
            self.draw_text(sb_strings.pr_cant)

    def prepare(self, msx, msy, sender):
        if self.firstset < GameBoard._shipsCount:
            self.myBoard.unhide()
            if sender == 1:
                self.position_result_handler(
                    self.myBoard.PvP(msx, msy, self.rank,
                                        self.hori, self.firstset))

        if self.firstset == GameBoard._shipsCount:
            self.myBoard.hide()
            self.draw_text(sb_strings.prepare10)
            self.firstset += 1
            return

        if self.firstset < GameBoard._shipsCountAll \
                and self.firstset >= GameBoard._shipsCount:
            self.hisBoard.unhide()
            if sender == 2:
                self.position_result_handler(
                    self.hisBoard.PvP(msx, msy, self.rank,
                                    self.hori, self.firstset))

        if self.firstset >= GameBoard._shipsCountAll:
            self.hisBoard.hide()
            self.draw_text(sb_strings.prepare_done)
            self.setHod(IGame.HOD_MY)

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
