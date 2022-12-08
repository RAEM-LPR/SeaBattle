from SB_game import IGame
from SB_game import SB_motion
from SB_board import GameBoard
from SB_board import GameTable
from SB_cell import CellState
from SB_helpers import SB_strings
from SB_link import SB_link
from SB_link import SB_attack_result
from SB_ship import ShipState
from SB_board import Ship_set_result


class Online_game(IGame):

    def __init__(self, mode=True):
        self.finished = False
        self.gameOver = False

        self.isMaster = mode
        self.myBoard = GameBoard(self.SENDER_MYBOARD)
        self.hisBoard = GameTable(self.SENDER_HISBOARD)
        self.firstset = 0
        self.motion = SB_motion.NONE
        self.myBoard.unhide()

        self.draw_text(SB_strings.letsbegin)

        SB_link.begin(mode)

    def setMotion(self, ipt):
        self.motion = ipt
        if ipt == SB_motion.HIS:
            self.draw_text(SB_strings.motionh)
        elif ipt == SB_motion.MY:
            self.draw_text(SB_strings.motionm)
        elif ipt == SB_motion.MY_WAIT:
            self.draw_text(SB_strings.motionw)

    def iteration(self):
        if SB_link.isHeLose:
            self.win()

        # если после завершения игры получили все неоткрытые палубы
        if SB_link.decks_tx_ended:
            for c in SB_link.decks_recieved:
                self.hisBoard.SetState(c.x, c.y, CellState.DECK)
            self.gameOver = True

        # ждём ответ от протиника, и он пришёл
        if self.getMotion() == SB_motion.MY_WAIT \
                and SB_link.attack_result != SB_attack_result.NONE:
            if SB_link.attack_result == SB_attack_result.MISS:
                self.setMotion(SB_motion.HIS)
                self.hisBoard.SetState(SB_link.his_attacked_deck.x,
                                       SB_link.his_attacked_deck.y,
                                       CellState.MISS)
            else:
                if SB_link.attack_result == SB_attack_result.DAMAGE:
                    self.hisBoard.damage(SB_link.his_attacked_deck.x,
                                         SB_link.his_attacked_deck.y)
                elif SB_link.attack_result == SB_attack_result.KILL:
                    self.hisBoard.kill(SB_link.his_attacked_deck.x,
                                       SB_link.his_attacked_deck.y)
                self.setMotion(SB_motion.MY)
            SB_link.attack_result = SB_attack_result.NONE
            SB_link.his_attacked_deck = None

        if self.getMotion() == SB_motion.HIS:  # если нас атакуют
            if SB_link.my_attacked_deck is not None:
                self.attack_me(SB_link.my_attacked_deck.x,
                               SB_link.my_attacked_deck.y)
                if self.myBoard.getShipState(
                        SB_link.my_attacked_deck.x,
                        SB_link.my_attacked_deck.y) == ShipState.SAFE:
                    self.setMotion(SB_motion.MY)
                    SB_link.result(SB_attack_result.MISS)
                else:
                    if self.myBoard.getShipState(
                            SB_link.my_attacked_deck.x,
                            SB_link.my_attacked_deck.y) == ShipState.HITTED:
                        SB_link.result(SB_attack_result.DAMAGE)
                    elif self.myBoard.getShipState(
                            SB_link.my_attacked_deck.x,
                            SB_link.my_attacked_deck.y) == ShipState.DESTROYED:
                        SB_link.result(SB_attack_result.KILL)
                    self.setMotion(SB_motion.HIS)
                SB_link.my_attacked_deck = None

        # если у нас не осталось кораблей
        if self.firstset >= GameTable._shipsCountAll:
            if self.myBoard.AllShipsDestroyed():
                self.lose()

    def attack_him(self, x, y):
        if self.hisBoard.getCell(x, y) == CellState.EMPTY \
                and self.getMotion() == SB_motion.MY:
            self.setMotion(SB_motion.MY_WAIT)
            SB_link.attack_result = SB_attack_result.NONE
            SB_link.attack(x, y)

    def pole_event(self, x, y, sender):
        """
        обработка клика на ячейку (x,y)
        игрового поля sender (наше или противника)
        """
        if self.myBoard.AllShipsDestroyed():
            return
        elif self.firstset < GameTable._shipsCountAll:
            if sender == self.SENDER_MYBOARD:
                self.set_ships(x, y, sender)
        elif self.getMotion() == SB_motion.MY:
            if sender == self.SENDER_HISBOARD:
                if SB_link.slaveReady:
                    self.attack_him(x, y)
                else:
                    self.draw_text(SB_strings.waittoset)

    def set_ships(self, x, y, sender):
        if self.firstset < GameBoard._shipsCount:
            if sender == self.SENDER_MYBOARD:
                self.position_result_handler(
                    self.myBoard.try_set_ship(
                        x, y, self.ship_rank,
                        self.ship_isHorisontal, self.firstset))

        if self.firstset == GameBoard._shipsCount:
            self.draw_text(SB_strings.prepare_done)
            self.firstset += 1
            self.setMotion(SB_motion.MY if self.isMaster else SB_motion.HIS)
            if not self.isMaster:
                SB_link.sendReadyFlag()

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

    def win(self):
        if self.gameOver:
            return
        self.sendShips()
        self.gameOver = True
        self.draw_text(SB_strings.win_link)

    def lose(self):
        if SB_link.isILose:
            return
        SB_link.lose()
        SB_link.isILose = True
        self.draw_text(SB_strings.lose_link)

    def sendShips(self):
        hideDecs = []
        for x in range(self.myBoard._size):
            for y in range(self.myBoard._size):
                if self.myBoard.getCell(x, y) == CellState.DECK:
                    hideDecs += [[x, y]]
        SB_link.sendDecks(hideDecs)


if __name__ == "__main__":
    print("This module is not for direct call!")
