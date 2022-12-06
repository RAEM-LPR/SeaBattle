import pygame

from SB_board import GameBoard
from SB_cell import CellState
from SB_helpers import sb_pair
from SB_helpers import sb_colors
from SB_game_online import Online_game
from SB_game_pvp import PVP_game


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
        SeaBattle.font_big = pygame.font.SysFont('Comic Sans MS', 45)
        SeaBattle.screen.fill(sb_colors.gray)
        pygame.display.set_caption('SeaBattle by RAEM-LPR')
        pygame.display.update()

        running = True
        online = True
        onlineMaster = True

        while running:
            SeaBattle.showintro()
            showing_intro = True

            while showing_intro:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        evpos = sb_pair(event.pos)

                        online = evpos.y > cls.SCREEN_HEIGHT / 2
                        onlineMaster = evpos.x < cls.SCREEN_WIDTH / 2
                        if evpos.y > cls.SCREEN_HEIGHT / 2 \
                                or evpos.x < cls.SCREEN_WIDTH / 2:
                            showing_intro = False

            cls.screen.fill(sb_colors.gray)

            if online:
                SeaBattle.game = Online_game(onlineMaster)
            else:
                SeaBattle.game = PVP_game()

            if SeaBattle.mainloop():
                pygame.quit()
                return

    @classmethod
    def showintro(cls):
        hw = cls.SCREEN_WIDTH / 2
        hh = cls.SCREEN_HEIGHT / 2

        cls.screen.fill(sb_colors.gray)
        cls.screen.fill(sb_colors.orange, (0, 0, hw, hh))
        cls.screen.fill(sb_colors.blue_ligth, (0, hh, hw, hh))
        cls.screen.fill(sb_colors.blue_dark, (hw, hh, hw, hh))
        cls.draw_text_big("Start offline", hw / 4, hh / 2)
        cls.draw_text_big("Create online", hw / 4, 3 * hh / 2)
        cls.draw_text_big("Join online", hw + hw / 4, 3 * hh / 2)

        pygame.display.update()

    @classmethod
    def mainloop(cls):
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

            if cls.game.draw_text_buffer is not None:
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
                and pos.x <= SeaBattle.game.hisBoard._size * cls.cellSize + \
                    cls.pos_hisBoard.x \
                and pos.y >= cls.pos_hisBoard.y \
                and pos.y <= \
                SeaBattle.game.hisBoard._size * cls.cellSize + \
                    cls.pos_hisBoard.y:

            pos.x -= cls.pos_hisBoard.x
            pos.y -= cls.pos_hisBoard.y
            SeaBattle.game.pole_event(pos.x // cls.cellSize,
                                      pos.y // cls.cellSize,
                                      SeaBattle.game.SENDER_HISBOARD)

        elif pos.x >= cls.pos_myBoard.x \
                and pos.x <= SeaBattle.game.myBoard._size * cls.cellSize + \
                    cls.pos_myBoard.x \
                and pos.y >= cls.pos_myBoard.y \
                and pos.y <= SeaBattle.game.myBoard._size * cls.cellSize + \
                    cls.pos_myBoard.y:

            pos.x -= cls.pos_myBoard.x
            pos.y -= cls.pos_myBoard.y
            SeaBattle.game.pole_event(pos.x // cls.cellSize,
                                      pos.y // cls.cellSize,
                                      SeaBattle.game.SENDER_MYBOARD)

    @classmethod
    def key_event(cls, event):
        if event.unicode == '1':
            SeaBattle.game.ship_rank = 1
        elif event.unicode == '2':
            SeaBattle.game.ship_rank = 2
        elif event.unicode == '3':
            SeaBattle.game.ship_rank = 3
        elif event.unicode == '4':
            SeaBattle.game.ship_rank = 4
        elif event.unicode == '5':
            SeaBattle.game.ship_isHorisontal = \
                not SeaBattle.game.ship_isHorisontal

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

    @classmethod
    def draw_text_big(cls, str, x, y):
        cls.screen.blit(
            cls.font_big.render(str, False, sb_colors.black), (x, y))


if __name__ == "__main__":
    SeaBattle.run()
