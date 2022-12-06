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

        self.myBoard.unhide()

        sb_link.begin(mode)

    def setHod(self, ipt): 
        if ipt == self.HOD_HIS or ipt == self.HOD_MY_WAIT: #FIXME dbg only
            sb_link._DBGWAITFLAG = True
        else:
            sb_link._DBGWAITFLAG = False

        self.hod = ipt
        if ipt == self.HOD_HIS:
            self.draw_text(sb_strings.hodh)
        elif ipt == self.HOD_MY:
            self.draw_text(sb_strings.hodm)
        elif ipt == self.HOD_MY_WAIT:
            self.draw_text(sb_strings.hodw)

    def iteration(self):
        if sb_link._DBGWAITFLAG:
            sb_link._DBGWAITFLAG = False
            sb_link.parse(input()) #FIXME DUBUG
            
        if sb_link.lheLose:
            self.win()
            self.gameOver = True

        if self.getHod() == self.HOD_MY_WAIT:
            if sb_link.lresult == 0:
                self.setHod(self.HOD_HIS)
                self.hisBoard.SetState(sb_link.lattack.x,sb_link.lattack.y,CellState.Miss)
            else:
                if sb_link.lresult == 1:
                    self.hisBoard.SetState(sb_link.lattack.x,sb_link.lattack.y,CellState.HitDeck)
                elif sb_link.lresult == 2:
                    self.hisBoard.kill(sb_link.lattack.x,sb_link.lattack.y)
                self.setHod(self.HOD_MY)
            sb_link.lresult = -2
            sb_link.lattack = None

        if self.getHod() == self.HOD_HIS:
            if not sb_link.lshoot is None:
                ttt = self.attack_me(sb_link.lshoot.x, sb_link.lshoot.y)
                if self.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.Safe:
                    self.setHod(self.HOD_MY)
                    sb_link.result(0)
                else:
                    if self.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.ShipHit:                     
                        sb_link.result(1)
                    elif self.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.Destroyed:
                        sb_link.result(2)
                    self.setHod(self.HOD_HIS)
                sb_link.lshoot = None

        if self.firstset >= GameTable._shipsCountAll:
            if self.myBoard.AllShipsDestroyed():
                self.lose()
                self.gameOver = True

    def attack_him(self, x, y):
        if self.hisBoard.getCell(x, y) == CellState.Empty \
                and self.getHod() == self.HOD_MY:
            self.setHod(self.HOD_MY_WAIT)
            sb_link.lresult = -1
            sb_link.attack(x, y)

    def pole_event(self, x, y, sender):
        if self.myBoard.AllShipsDestroyed():
            return
        elif self.firstset < GameTable._shipsCountAll:
            if sender == self.SENDER_MYBOARD:
                self.prepare(x, y, sender)
        elif self.getHod() == self.HOD_MY:
            if sender == self.SENDER_HISBOARD:
                self.attack_him(x, y)

    def prepare(self, x, y, sender):
        if self.firstset < GameBoard._shipsCount:
            if sender == self.SENDER_MYBOARD:
                self.position_result_handler(
                    self.myBoard.PvP(x, y, self.rank,
                                     self.hori, self.firstset))

        if self.firstset == GameBoard._shipsCount:
            self.draw_text(sb_strings.prepare_done)
            self.firstset += 1
            self.setHod(self.HOD_MY if self.isMaster else self.HOD_HIS)


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

            

if __name__ == "__main__":
    print("This module is not for direct call!")
