import pygame

from sb_board import GameBoard
from sb_board import GameTable
from sb_board import pvp_result
from sb_cell import CellState
from sb_helpers import sb_pair
from sb_helpers import sb_colors
from sb_helpers import sb_strings
from sb_link import sb_link
from sb_ship import ShipState

class SeaBattle: #it will be main class
    ...

class Game:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 500
    pos_myBoard = sb_pair((40, 40))
    pos_hisBoard = sb_pair((560, 40))
    pos_txt = sb_pair((10, 10))
    cellSize = 40
    FPS = 10

    myBoard = None
    hisBoard = None
    screen = None
    clock = None
    font = None
    firstset = 0
    link_mode = False

    @classmethod
    def run(cls):
        pygame.init()
        Game.screen = pygame.display.set_mode(
            (Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))

        Game.clock = pygame.time.Clock()
        Game.font = pygame.font.SysFont('Comic Sans MS', 15)
        Game.screen.fill(sb_colors.gray)

        
        """while Game.mainloop_pvp():
            ..."""
        while Game.mainloop_link():
            ...

        pygame.quit()

    @classmethod
    def mainloop_link(cls, isMain=True):
        finished = False
        gameOver = False
        isMaster = isMain # FIXME 
        Game.link_mode = True

        Game.myBoard = GameBoard()
        Game.hisBoard = GameTable()
        Game.firstset = 0
        Game.hod = Game.HOD_NONE

        Game.draw_text(sb_strings.letsbegin)
        pygame.display.update()

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if gameOver:
                        return True
                    Game.mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    Game.key_event(event)

            sb_link.parse(input())#FIXME DUBUG  если существует некий файл!!!
                
            #if sb_link.available: 
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

        return False

    @classmethod
    def mainloop_pvp(cls):
        finished = False
        gameOver = False

        Game.myBoard = GameBoard()
        Game.hisBoard = GameBoard()
        Game.firstset = 0
        Game.hod = Game.HOD_NONE

        Game.draw_text(sb_strings.letsbegin)
        pygame.display.update()

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if gameOver:
                        return True
                    Game.mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    Game.key_event(event)

            if Game.firstset >= GameBoard._shipsCountAll:
                if Game.myBoard.AllShipsDestroyed():
                    Game.lose()
                    gameOver = True
                if Game.hisBoard.AllShipsDestroyed():
                    Game.win()
                    gameOver = True

            # Game.screen.fill(colors.gray)
            Game.draw_cells()
            pygame.display.update()

            Game.clock.tick(Game.FPS)

        return False

    @classmethod
    def attack_him(cls, nx, ny):
        if Game.link_mode:
            if Game.hisBoard.getCell(nx,ny) != CellState.HitDeck \
                or Game.hisBoard.getCell(nx,ny) != CellState.Miss:
                    if sb_link.lresult == -2:
                        sb_link.lresult == -1
                        sb_link.attack(nx, ny)
            return
        if cls.hisBoard.getCell(ny, nx) == CellState.HitDeck \
                or cls.hisBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.hisBoard.Shoot(nx, ny)

    @classmethod
    def attack_me(cls, nx, ny):
        if cls.myBoard.getCell(ny, nx) == CellState.HitDeck \
                or cls.myBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.myBoard.Shoot(nx, ny)

    @classmethod
    def mouse_event(cls, event):
        pos = sb_pair(event.pos)
        if pos.x >= Game.pos_hisBoard.x \
                and pos.x <= \
                Game.hisBoard._size * Game.cellSize + Game.pos_hisBoard.x \
                and pos.y >= Game.pos_hisBoard.y \
                and pos.y <= \
                Game.hisBoard._size * Game.cellSize + Game.pos_hisBoard.y:

            pos.x -= Game.pos_hisBoard.x
            pos.y -= Game.pos_hisBoard.y
            return Game.pole_event(pos.x // Game.cellSize,
                                   pos.y // Game.cellSize, 2)

        elif pos.x >= Game.pos_myBoard.x and \
                pos.x <= \
                Game.myBoard._size * Game.cellSize + Game.pos_myBoard.x \
                and pos.y >= Game.pos_myBoard.y \
                and pos.y <= \
                Game.myBoard._size * Game.cellSize + Game.pos_myBoard.y:

            pos.x -= Game.pos_myBoard.x
            pos.y -= Game.pos_myBoard.y
            return Game.pole_event(pos.x // Game.cellSize,
                                   pos.y // Game.cellSize, 1)

        return True

    @classmethod
    def pole_event(cls, y, x, sender):
        if Game.link_mode:
            return Game.pole_event_link(y, x, sender)
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

    @classmethod
    def pole_event_link(cls, y, x, sender):
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

    @classmethod
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

    @classmethod
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

        if not Game.link_mode:
            

            if Game.firstset < GameBoard._shipsCountAll \
                    and Game.firstset >= GameBoard._shipsCount:
                Game.hisBoard.unhide()
                if sender == 2:
                    Game.pvp_result_handler(
                        Game.hisBoard.PvP(msx, msy, Game.rank,
                                        Game.hori, Game.firstset))

        elif Game.firstset==10:
            Game.firstset =21
            Game.myBoard.unhide()

        if Game.firstset >= GameBoard._shipsCountAll:
            Game.hisBoard.hide()
            Game.draw_text(sb_strings.prepare_done)
            Game.setHod(Game.HOD_MY)

    rank = 0
    hori = 0

    @classmethod
    def key_event(cls, event):
        if event.unicode == '1':
            Game.rank = 1
        elif event.unicode == '2':
            Game.rank = 2
        elif event.unicode == '3':
            Game.rank = 3
        elif event.unicode == '4':
            Game.rank = 4
        elif event.unicode == '5':
            Game.hori = 1 - Game.hori

    HOD_NONE = 0
    HOD_MY = 1
    HOD_HIS = 2
    hod = HOD_NONE

    @classmethod
    def setHod(cls, ipt):
        Game.hod = ipt

    @classmethod
    def getHod(cls):
        return Game.hod

    @classmethod
    def checkWin(cls):
        return Game.myBoard.AllShipsDestroyed() \
                or Game.myBoard.AllShipsDestroyed()

    @classmethod
    def win(cls):
        Game.myBoard.unhide()
        Game.hisBoard.unhide()
        Game.draw_text(sb_strings.win)

    @classmethod
    def win_link(cls):
        Game.draw_text(sb_strings.win)
        #FIXME

    @classmethod
    def lose(cls):
        Game.myBoard.unhide()
        Game.hisBoard.unhide()
        Game.draw_text(sb_strings.lose)

    @classmethod
    def lose_link(cls):
        Game.myBoard.unhide()
        #FIXME

    @classmethod
    def draw_cells(cls, unhide=True):
        px = Game.cellSize

        for i in range(GameBoard._size):
            for j in range(GameBoard._size):
                thiscolor = sb_colors.blue_dark
                if Game.myBoard.getCell(i, j) == CellState.Deck:
                    if unhide:
                        thiscolor = sb_colors.orange
                    else:
                        thiscolor = sb_colors.blue_dark
                elif Game.myBoard.getCell(i, j) == CellState.Empty:
                    thiscolor = sb_colors.blue_dark
                elif Game.myBoard.getCell(i, j) == CellState.HitDeck:
                    thiscolor = sb_colors.red
                elif Game.myBoard.getCell(i, j) == CellState.Miss:
                    thiscolor = sb_colors.blue_ligth

                pygame.draw.rect(Game.screen, thiscolor, (
                    Game.pos_myBoard.x + i * px,
                    Game.pos_myBoard.y + j * px, px, px))

                if Game.hisBoard.getCell(i, j) == CellState.Deck:
                    if unhide:
                        thiscolor = sb_colors.orange
                    else:
                        thiscolor = sb_colors.blue_dark
                elif Game.hisBoard.getCell(i, j) == CellState.Empty:
                    thiscolor = sb_colors.blue_dark
                elif Game.hisBoard.getCell(i, j) == CellState.HitDeck:
                    thiscolor = sb_colors.red
                elif Game.hisBoard.getCell(i, j) == CellState.Miss:
                    thiscolor = sb_colors.blue_ligth

                pygame.draw.rect(Game.screen, thiscolor, (
                    Game.pos_hisBoard.x + i * px,
                    Game.pos_hisBoard.y + j * px, px, px))

        Game.draw_hash(Game.myBoard, Game.pos_myBoard)
        Game.draw_hash(Game.hisBoard, Game.pos_hisBoard)

    @classmethod
    def draw_text(cls, str, color=sb_colors.black, coord=None):
        if coord is None:
            coord = Game.pos_txt
        Game.screen.fill(sb_colors.gray)
        Game.draw_cells()
        Game.screen.blit(
            Game.font.render(str, False, color), (coord.x, coord.y))

    @classmethod
    def draw_hash(cls, board, boardpos):
        for i in range(board._size + 1):
            px = Game.cellSize
            si = board._size
            x = boardpos.x
            y = boardpos.y
            pygame.draw.line(Game.screen, sb_colors.black,
                             (x + i * px, y + 0),
                             (x + i * px, y + si * px))
            pygame.draw.line(Game.screen, sb_colors.black,
                             (x + 0, y + i * px),
                             (x + si * px, y + i * px))


if __name__ == "__main__":
    Game.run()
