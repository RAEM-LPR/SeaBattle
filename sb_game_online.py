from sb_game import IGame
from sb_board import GameBoard
from sb_board import GameTable
from sb_cell import CellState
from sb_helpers import sb_pair
from sb_helpers import sb_colors
from sb_helpers import sb_strings
from sb_link import sb_link
from sb_ship import ShipState
from sb_board import pvp_result


class Online_game(IGame):

    HOD_MY_WAIT = 3

    def __init__(self, mode=True):
        self.finished = False
        self.gameOver = False

        self.isMaster = mode
        self.myBoard = GameBoard()
        self.hisBoard = GameTable()
        self.firstset = 0
        self.hod = IGame.HOD_NONE

        sb_link.begin(mode)

    def setHod(self, ipt): #FIXME dbg only
        if ipt == self.HOD_HIS and not sb_link._DBGWAITFLAG:
            sb_link._DBGWAITFLAG = True
        self.hod = ipt

    def iteration(self):
        if sb_link._DBGWAITFLAG:
            sb_link._DBGWAITFLAG = False
            sb_link.parse(input()) #FIXME DUBUG
            
        if sb_link.lheLose:
            self.win()
            self.gameOver = True

        if sb_link.lresult != -2:
            if sb_link.lresult == 0:
                self.setHod(self.HOD_HIS)
                sb_link.lresult = -2
                self.hisBoard.SetState(sb_link.lattack.x,sb_link.lattack.y,CellState.Miss)
                del sb_link.lattack
            elif sb_link.lresult == 1:
                self.setHod(self.HOD_MY)
                sb_link.lresult = -2
                self.hisBoard.SetState(sb_link.lattack.x,sb_link.lattack.y,CellState.HitDeck)
                del sb_link.lattack
            elif sb_link.lresult == 2:
                self.setHod(self.HOD_MY)
                sb_link.lresult = -2
                self.hisBoard.kill(sb_link.lattack.x,sb_link.lattack.y)
                del sb_link.lattack

        if self.getHod() == self.HOD_HIS:
            if not sb_link.lshoot is None:
                self.attack_me(sb_link.lshoot.x, sb_link.lshoot.y)
                if self.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.Safe:
                    self.setHod(self.HOD_MY)
                    del sb_link.lshoot
                    sb_link.result(0)
                elif self.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.ShipHit:
                    self.setHod(self.HOD_HIS)
                    del sb_link.lshoot
                    sb_link.result(1)
                elif self.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.Destroyed:
                    self.setHod(self.HOD_HIS)
                    del sb_link.lshoot
                    sb_link.result(2)
                    
        if self.firstset >= GameTable._shipsCountAll:
            if self.myBoard.AllShipsDestroyed():
                self.lose()
                self.gameOver = True

    def attack_him(self, nx, ny):
        if self.hisBoard.getCell(nx,ny) != CellState.HitDeck \
            and self.hisBoard.getCell(nx,ny) != CellState.Miss:
                if sb_link.lresult == -2:
                    sb_link.lresult == -1
                    sb_link.attack(nx, ny)

    def pole_event(self, y, x, sender):
        if self.myBoard.AllShipsDestroyed():
            return True
        if self.firstset < GameTable._shipsCountAll:
            if sender == 1:
                self.prepare(x, y, sender)
                return True
        elif self.getHod() == self.HOD_MY:
            if sender == 2:
                if not self.attack_him(x, y):
                    self.draw_text(sb_strings.hod2)
                    self.setHod(self.HOD_HIS)
                    return True
        return False

    def prepare(self, msx, msy, sender):
        if self.firstset < GameBoard._shipsCount:
            self.myBoard.unhide()
            if sender == 1:
                self.position_result_handler(
                    self.myBoard.PvP(msx, msy, self.rank,
                                     self.hori, self.firstset))

        if self.firstset == GameBoard._shipsCount:
            #self.myBoard.hide()
            self.draw_text(sb_strings.prepare10)#Game.draw_text(sb_strings.prepare_done)
            self.firstset += 1
            self.setHod(self.HOD_MY if self.isMaster else self.HOD_HIS)
            """if self.isMaster:
                self.setHod(self.HOD_MY)
            else:
                self.setHod(self.HOD_MY)
            return"""

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

            

if __name__ == "__main__":
    print("This module is not for direct call!")
