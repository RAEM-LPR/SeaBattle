from SB_game import IGame
from SB_game import sb_motion
from SB_board import GameBoard
from SB_board import GameTable
from SB_cell import CellState
from SB_helpers import sb_strings
from SB_link import sb_link
from SB_link import sb_attack_result
from SB_ship import ShipState
from SB_board import ship_set_result


class Online_game(IGame):

    def __init__(self, mode=True):
        self.finished = False
        self.gameOver = False

        self.isMaster = mode
        self.myBoard = GameBoard()
        self.hisBoard = GameTable()
        self.firstset = 0
        self.motion = sb_motion.NONE

        self.myBoard.unhide()

        sb_link.begin(mode)

    def setMotion(self, ipt):
        self.motion = ipt
        if ipt == sb_motion.HIS:
            self.draw_text(sb_strings.motionh)
        elif ipt == sb_motion.MY:
            self.draw_text(sb_strings.motionm)
        elif ipt == sb_motion.MY_WAIT:
            self.draw_text(sb_strings.motionw)

    def iteration(self):
        if sb_link.isHeLose:
            self.win()

        if sb_link.decks_tx_ended:
            for c in sb_link.decks_recieved:
                self.hisBoard.SetState(c.x, c.y, CellState.Deck)
            self.gameOver = True

        if self.getMotion() == sb_motion.MY_WAIT:
            if sb_link.attack_result == sb_attack_result.MISS:
                self.setMotion(sb_motion.HIS)
                self.hisBoard.SetState(sb_link.his_attacked_deck.x,
                                       sb_link.his_attacked_deck.y,
                                       CellState.Miss)
            else:
                if sb_link.attack_result == sb_attack_result.DAMAGE:
                    self.hisBoard.SetState(sb_link.his_attacked_deck.x,
                                           sb_link.his_attacked_deck.y,
                                           CellState.HitDeck)
                elif sb_link.attack_result == sb_attack_result.KILL:
                    self.hisBoard.kill(sb_link.his_attacked_deck.x,
                                       sb_link.his_attacked_deck.y)
                self.setMotion(sb_motion.MY)
            sb_link.attack_result = sb_attack_result.NONE
            sb_link.his_attacked_deck = None

        if self.getMotion() == sb_motion.HIS:
            if sb_link.my_attacked_deck is not None:
                self.attack_me(sb_link.my_attacked_deck.x,
                               sb_link.my_attacked_deck.y)
                if self.myBoard.getShipState(
                        sb_link.my_attacked_deck.x,
                        sb_link.my_attacked_deck.y) == ShipState.Safe:
                    self.setMotion(sb_motion.MY)
                    sb_link.result(0)
                else:
                    if self.myBoard.getShipState(
                            sb_link.my_attacked_deck.x,
                            sb_link.my_attacked_deck.y) == ShipState.ShipHit:
                        sb_link.result(1)
                    elif self.myBoard.getShipState(
                            sb_link.my_attacked_deck.x,
                            sb_link.my_attacked_deck.y) == ShipState.Destroyed:
                        sb_link.result(2)
                    self.setMotion(sb_motion.HIS)
                sb_link.my_attacked_deck = None

        if self.firstset >= GameTable._shipsCountAll:
            if self.myBoard.AllShipsDestroyed():
                self.lose()

    def attack_him(self, x, y):
        if self.hisBoard.getCell(x, y) == CellState.Empty \
                and self.getMotion() == sb_motion.MY:
            self.setMotion(sb_motion.MY_WAIT)
            sb_link.attack_result = sb_attack_result.NONE
            sb_link.attack(x, y)

    def pole_event(self, x, y, sender):
        if self.myBoard.AllShipsDestroyed():
            return
        elif self.firstset < GameTable._shipsCountAll:
            if sender == self.SENDER_MYBOARD:
                self.set_ships(x, y, sender)
        elif self.getMotion() == sb_motion.MY:
            if sender == self.SENDER_HISBOARD:
                self.attack_him(x, y)

    def set_ships(self, x, y, sender):
        if self.firstset < GameBoard._shipsCount:
            if sender == self.SENDER_MYBOARD:
                self.position_result_handler(
                    self.myBoard.try_set_ship(
                        x, y, self.ship_rank,
                        self.ship_isHorisontal, self.firstset))

        if self.firstset == GameBoard._shipsCount:
            self.draw_text(sb_strings.prepare_done)
            self.firstset += 1
            self.setMotion(sb_motion.MY if self.isMaster else sb_motion.HIS)

    def position_result_handler(self, result):
        if result == ship_set_result.ok:
            self.firstset += 1
            self.draw_text('')
        elif result == ship_set_result.incorrect:
            self.draw_text(sb_strings.pr_incorrect)
        elif result == ship_set_result.out_of_pole:
            self.draw_text(sb_strings.pr_out)
        elif result == ship_set_result.overflow:
            self.draw_text(sb_strings.pr_ovf)
        elif result == ship_set_result.cant_pos:
            self.draw_text(sb_strings.pr_cant)

    def win(self):
        if self.gameOver:
            return
        self.sendShips()
        self.gameOver = True

    def lose(self):
        if sb_link.isILose:
            return
        sb_link.lose()
        sb_link.isILose = True

    def sendShips(self):
        hideDecs = []
        for x in range(self.myBoard._size):
            for y in range(self.myBoard._size):
                if self.myBoard.getCell(x, y) == CellState.Deck:
                    hideDecs += [[x, y]]
        sb_link.sendDecks(hideDecs)


if __name__ == "__main__":
    print("This module is not for direct call!")
