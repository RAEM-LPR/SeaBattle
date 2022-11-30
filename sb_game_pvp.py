
from sb_board import GameBoard
from sb_board import GameTable
from sb_board import pvp_result
from sb_cell import CellState
from sb_helpers import sb_pair
from sb_helpers import sb_colors
from sb_helpers import sb_strings
from sb_link import sb_link
from sb_ship import ShipState


class Pvp_game(Game):

    def mainloop(self , param): # FIXME param: screen fps clock
        finished = False
        gameOver = False

        self.myBoard = GameBoard()
        self.hisBoard = GameBoard()
        self.firstset = 0
        self.hod = Game.HOD_NONE

        self.draw_text(sb_strings.letsbegin)
        self.upd()#pygame.display.update()

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if gameOver:
                    self.mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    self.key_event(event)

            if self.firstset >= GameBoard._shipsCountAll:
                if self.myBoard.AllShipsDestroyed():
                    self.lose()
                    gameOver = True
                if self.hisBoard.AllShipsDestroyed():
                    self.win()
                    gameOver = True

            # Game.screen.fill(colors.gray)
            self.draw_cells()
            self.upd()
            self.tick()

def attack_him(cls, nx, ny):
    if cls.hisBoard.getCell(ny, nx) == CellState.HitDeck \
            or cls.hisBoard.getCell(ny, nx) == CellState.Miss:
        return True
    return cls.hisBoard.Shoot(nx, ny)

def pole_event(cls, y, x, sender):
    if Game.checkWin():
        return True
    if Game.firstset < GameBoard._shipsCountAll:
        Game.prepare(x, y, sender)
        return True
    elif Game.getHod() == Game.HOD_MY:
        if sender == 2:
            if not Game.attack_him(x, y):
                Game.draw_text(sb_strings.hod2)
                Game.setHod(Game.HOD_HIS)
                return True
        else:
            return False
    elif Game.getHod() == Game.HOD_HIS:
        if sender == 1:
            if not Game.attack_me(x, y):
                Game.draw_text(sb_strings.hod1)
                Game.setHod(Game.HOD_MY)
                return True
        else:
            return False
    if Game.checkWin():
        return True
    return False

def pvp_result_handler(cls, result):
    if result == pvp_result.ok:
        Game.firstset += 1
        Game.screen.fill(sb_colors.gray)
    elif result == pvp_result.incorrect:
        Game.draw_text(sb_strings.pr_incorrect)
    elif result == pvp_result.out_of_pole:
        Game.draw_text(sb_strings.pr_out)
    elif result == pvp_result.overflow:
        Game.draw_text(sb_strings.pr_ovf)
    elif result == pvp_result.cant_pos:
        Game.draw_text(sb_strings.pr_cant)

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

    

    if Game.firstset < GameBoard._shipsCountAll \
            and Game.firstset >= GameBoard._shipsCount:
        Game.hisBoard.unhide()
        if sender == 2:
            Game.pvp_result_handler(
                Game.hisBoard.PvP(msx, msy, Game.rank,
                                Game.hori, Game.firstset))

    if Game.firstset >= GameBoard._shipsCountAll:
        Game.hisBoard.hide()
        Game.draw_text(sb_strings.prepare_done)
        Game.setHod(Game.HOD_MY)

def win(cls):
    Game.myBoard.unhide()
    Game.hisBoard.unhide()
    Game.draw_text(sb_strings.win)

def lose(cls):
    Game.myBoard.unhide()
    Game.hisBoard.unhide()
    Game.draw_text(sb_strings.lose)
