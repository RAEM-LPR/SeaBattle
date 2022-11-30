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

#from sb_game_online import Online_game
from sb_game_pvp import Pvp_game


class SeaBattle:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 500
    pos_myBoard = sb_pair((40, 40))
    pos_hisBoard = sb_pair((560, 40))
    pos_txt = sb_pair((10, 10))
    cellSize = 40
    FPS = 10

    game = None
    screen = None
    clock = None
    font = None
    firstset = 0
    link_mode = False

    @classmethod
    def run(cls):
        pygame.init()
        SeaBattle.screen = pygame.display.set_mode(
            (cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT))

        SeaBattle.clock = pygame.time.Clock()
        SeaBattle.font = pygame.font.SysFont('Comic Sans MS', 15)
        SeaBattle.screen.fill(sb_colors.gray)

        running = True
        online = False

        while running:
            cls.screen.fill(sb_colors.gray)
            if online:
                pass #SeaBattle.game = Online_game()
            else:
                SeaBattle.game = Pvp_game()
            
            if SeaBattle.mainloop():
                pygame.quit()
                return
        

    @classmethod
    def mainloop(cls):
        cls.draw_text(sb_strings.letsbegin)
        pygame.display.update()
        #notfinished = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if SeaBattle.game.gameOver:
                        return False
                    SeaBattle.mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    SeaBattle.key_event(event)
            
            if not cls.game.draw_text_buffer is None:
                cls.screen.fill(sb_colors.gray)
                cls.draw_text(cls.game.draw_text_buffer)
                cls.game.draw_text_buffer = None
                cls.draw_cells()

            pygame.display.update()
            SeaBattle.game.iteration()
            cls.draw_cells()
            cls.clock.tick(cls.FPS)
            pygame.display.update()

    @classmethod 
    def mouse_event(cls, event):
        pos = sb_pair(event.pos)
        if pos.x >= cls.pos_hisBoard.x \
                and pos.x <= \
                SeaBattle.game.hisBoard._size * cls.cellSize + cls.pos_hisBoard.x \
                and pos.y >= cls.pos_hisBoard.y \
                and pos.y <= \
                SeaBattle.game.hisBoard._size * cls.cellSize + cls.pos_hisBoard.y:

            pos.x -= cls.pos_hisBoard.x
            pos.y -= cls.pos_hisBoard.y
            return SeaBattle.game.pole_event(pos.x // cls.cellSize,
                                   pos.y // cls.cellSize, 2)

        elif pos.x >= cls.pos_myBoard.x and \
                pos.x <= \
                SeaBattle.game.myBoard._size * cls.cellSize + cls.pos_myBoard.x \
                and pos.y >= cls.pos_myBoard.y \
                and pos.y <= \
                SeaBattle.game.myBoard._size * cls.cellSize + cls.pos_myBoard.y:

            pos.x -= cls.pos_myBoard.x
            pos.y -= cls.pos_myBoard.y
            return SeaBattle.game.pole_event(pos.x // cls.cellSize,
                                   pos.y // cls.cellSize, 1)

        return True

    @classmethod 
    def key_event(cls, event):
        if event.unicode == '1':
            SeaBattle.game.rank = 1
        elif event.unicode == '2':
            SeaBattle.game.rank = 2
        elif event.unicode == '3':
            SeaBattle.game.rank = 3
        elif event.unicode == '4':
            SeaBattle.game.rank = 4
        elif event.unicode == '5':
            SeaBattle.game.hori = 1 - SeaBattle.game.hori      

    @classmethod
    def draw_cells(cls, unhide=True):
        px = cls.cellSize

        for i in range(GameBoard._size):
            for j in range(GameBoard._size):
                thiscolor = sb_colors.blue_dark
                thiscell = SeaBattle.game.myBoard.getCell(i, j)
                if thiscell == CellState.Deck:
                    if unhide:
                        thiscolor = sb_colors.orange
                    else:
                        thiscolor = sb_colors.blue_dark
                elif thiscell == CellState.Empty:
                    thiscolor = sb_colors.blue_dark
                elif thiscell == CellState.HitDeck:
                    thiscolor = sb_colors.red
                elif thiscell == CellState.Miss:
                    thiscolor = sb_colors.blue_ligth

                pygame.draw.rect(cls.screen, thiscolor, (
                    cls.pos_myBoard.x + i * px,
                    cls.pos_myBoard.y + j * px, px, px))

                thiscell = SeaBattle.game.hisBoard.getCell(i, j)
                if thiscell == CellState.Deck:
                    if unhide:
                        thiscolor = sb_colors.orange
                    else:
                        thiscolor = sb_colors.blue_dark
                elif thiscell == CellState.Empty:
                    thiscolor = sb_colors.blue_dark
                elif thiscell == CellState.HitDeck:
                    thiscolor = sb_colors.red
                elif thiscell == CellState.Miss:
                    thiscolor = sb_colors.blue_ligth

                pygame.draw.rect(cls.screen, thiscolor, (
                    cls.pos_hisBoard.x + i * px,
                    cls.pos_hisBoard.y + j * px, px, px))

        cls.draw_hash(SeaBattle.game.myBoard, cls.pos_myBoard)
        cls.draw_hash(SeaBattle.game.hisBoard, cls.pos_hisBoard)

    @classmethod
    def draw_hash(cls, board, boardpos):
        for i in range(board._size + 1):
            px = cls.cellSize
            si = board._size
            x = boardpos.x
            y = boardpos.y
            pygame.draw.line(cls.screen, sb_colors.black,
                             (x + i * px, y + 0),
                             (x + i * px, y + si * px))
            pygame.draw.line(cls.screen, sb_colors.black,
                             (x + 0, y + i * px),
                             (x + si * px, y + i * px))

    @classmethod
    def draw_text(cls, str, color=sb_colors.black, coord=None):
        if coord is None:
            coord = cls.pos_txt
        cls.screen.fill(sb_colors.gray)
        cls.draw_cells()
        cls.screen.blit(
            cls.font.render(str, False, color), (coord.x, coord.y))                          


if __name__ == "__main__":
    SeaBattle.run()
