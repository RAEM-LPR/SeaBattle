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

from sb_game import Online_game
from sb_game import Pvp_game



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
            (SeaBattle.SCREEN_WIDTH, SeaBattle.SCREEN_HEIGHT))

        SeaBattle.clock = pygame.time.Clock()
        SeaBattle.font = pygame.font.SysFont('Comic Sans MS', 15)
        SeaBattle.screen.fill(sb_colors.gray)

        running = True
        online = False

        while running:
            if online:
                SeaBattle.game = Online_game()
            else:
                SeaBattle.game = Pvp_game()

        SeaBattle.game.mainloop()

        pygame.quit()

"""class _Game:
    


    def checkWin(cls):
        return Game.myBoard.AllShipsDestroyed() \
                or Game.myBoard.AllShipsDestroyed()

    def win_link(cls):
        Game.draw_text(sb_strings.win)
        #FIXME


    def lose_link(cls):
        Game.myBoard.unhide()
        #FIXME
"""



if __name__ == "__main__":
    SeaBattle.run()
