
#from sb_game import Game

from sb_board import GameBoard
from sb_board import GameTable
from sb_board import pvp_result
from sb_cell import CellState
from sb_helpers import sb_pair
from sb_helpers import sb_colors
from sb_helpers import sb_strings
from sb_link import sb_link
from sb_ship import ShipState

import os #ddd FIXME

class Online_game(gGame):

    def __init__(self, _screen, _clock, _font):
        self.screen = _screen
        self.clock = _clock
        self.font = _font

        self.finished = False
        self.gameOver = False

        self.isMaster = True # FIXME 
        self.myBoard = GameBoard()
        self.hisBoard = GameBoard()
        self.firstset = 0
        self.hod = super.HOD_NONE
  
    def mainloop(self): 


        Game.draw_text(sb_strings.letsbegin)
        self.upd()

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if gameOver:
                        #return True
                    Game.mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    Game.key_event(event)

            try:
                file = open('i')
            except IOError:
                ...
            else:
                os.rename('i','ii')
                sb_link.parse(input()) #FIXME DUBUG  если существует некий файл!!!
                
            if sb_link.lheLose:
                Game.win_link()
                gameOver = True
            if sb_link.lresult == 0:
                Game.setHod(Game.HOD_HIS)
                sb_link.lresult = -2
            elif sb_link.lresult == 1:
                Game.setHod(Game.HOD_MY)
                sb_link.lresult = -2
                Game.hisBoard.SetState(sb_link.lattack.x,sb_link.lattack.y,CellState.HitDeck)
                del sb_link.lattack
            elif sb_link.lresult == 2:
                Game.setHod(Game.HOD_MY)
                sb_link.lresult = -2
                Game.hisBoard.kill(sb_link.lattack.x,sb_link.lattack.y)
                del sb_link.lattack
            if Game.getHod() == Game.HOD_HIS:
                if not sb_link.lshoot is None:
                    Game.attack_me(sb_link.lshoot.x, sb_link.lshoot.y)
                    if Game.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.Safe:
                        Game.setHod(Game.HOD_MY)
                        del sb_link.lshoot
                        sb_link.result(0)
                    elif Game.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.ShipHit:
                        Game.setHod(Game.HOD_HIS)
                        del sb_link.lshoot
                        sb_link.result(1)
                    elif Game.myBoard.getShipState(sb_link.lshoot.x, sb_link.lshoot.y) == ShipState.Destroyed:
                        Game.setHod(Game.HOD_HIS)
                        del sb_link.lshoot
                        sb_link.result(2)

            if Game.firstset >= GameBoard._shipsCountAll:
                if Game.myBoard.AllShipsDestroyed():
                    Game.lose_link()
                    gameOver = True

            Game.draw_cells()
            pygame.display.update()

            Game.clock.tick(Game.FPS)

        #return False

    def attack_him(cls, nx, ny):
        if Game.hisBoard.getCell(nx,ny) != CellState.HitDeck \
            or Game.hisBoard.getCell(nx,ny) != CellState.Miss:
                if sb_link.lresult == -2:
                    sb_link.lresult == -1
                    sb_link.attack(nx, ny)

    def pole_event(cls, y, x, sender):
        if Game.myBoard.AllShipsDestroyed():
            return True
        if Game.firstset < GameBoard._shipsCountAll:
            if sender == 1:
                Game.prepare(x, y, sender)
                return True
        elif Game.getHod() == Game.HOD_MY:
            if sender == 2:
                if not Game.attack_him_link(x, y):
                    Game.draw_text(sb_strings.hod2)
                    Game.setHod(Game.HOD_HIS)
                    return True
        return False

    def prepare(cls, msx, msy, sender):
        if Game.firstset < GameBoard._shipsCount:
            Game.myBoard.unhide()
            if sender == 1:
                Game.pvp_result_handler(
                    Game.myBoard.PvP(msx, msy, Game.rank,
                                     Game.hori, Game.firstset))

        if Game.firstset == GameBoard._shipsCount:
            Game.myBoard.hide()
            Game.draw_text(sb_strings.prepare10)
            Game.firstset += 1
            return


        Game.firstset==10 # FIXME
        Game.firstset =21
        Game.myBoard.unhide()

        if Game.firstset >= GameBoard._shipsCountAll:
            Game.hisBoard.hide()
            Game.draw_text(sb_strings.prepare_done)
            Game.setHod(Game.HOD_MY)

if __name__ == "__main__":
    print("This module is not for direct call!")
