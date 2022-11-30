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


class __Game:
    myBoard = None
    hisBoard = None

    rank = 0
    hori = 0

    HOD_NONE = 0
    HOD_MY = 1
    HOD_HIS = 2
    hod = HOD_NONE

    def mainloop(self):
        ...
    def attack_him(cls, nx, ny):
        ...
    
    def attack_me(cls, nx, ny):
        if cls.myBoard.getCell(ny, nx) == CellState.HitDeck \
                or cls.myBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.myBoard.Shoot(nx, ny)

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

    def pole_event(cls, y, x, sender):
        ...
    def prepare(cls, msx, msy, sender):
        ...
    HOD_NONE = 0
    HOD_MY = 1
    HOD_HIS = 2
    hod = HOD_NONE

    def setHod(cls, ipt):
        Game.hod = ipt

    def getHod(cls):
        return Game.hod

    def checkWin(cls):
        ...# return Game.myBoard.AllShipsDestroyed() or Game.myBoard.AllShipsDestroyed()

    def win(cls):
        ...

    def lose(cls):
        ...

    def draw_cells(cls, unhide=True):
        ...

    def upd(cls):
        pygame.display.update()

    def tick(cls)
        cls.clock.tick(cls.FPS)

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

    def draw_text(cls, str, color=sb_colors.black, coord=None):
        if coord is None:
            coord = Game.pos_txt
        Game.screen.fill(sb_colors.gray)
        Game.draw_cells()
        Game.screen.blit(
            Game.font.render(str, False, color), (coord.x, coord.y))


