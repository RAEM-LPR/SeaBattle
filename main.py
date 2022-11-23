#import pubnub
import pygame

from helpers import *
from cell import * 
from ship import *
from board import *

class game:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 500
    FPS = 10
    pos_myBoard = pair((40,40))
    pos_hisBoard = pair((560,40))
    cellSize = 40

    myBoard = None
    hisBoard = None
    screen = None
    clock = None
    firstset = 0
    
    """
    def __init__(self):
        ... #init pygame
    """
    @classmethod
    def run(cls):
        pygame.init()
        game.screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        
        game.clock = pygame.time.Clock()
        game.screen.fill(color.gray)

        
        game.mainloop()

        pygame.quit()

    @classmethod
    def mainloop(cls):
        finished = False

        game.myBoard = gameBoard()
        game.hisBoard = gameBoard()
        game.myBoard.Generate()
        game.hisBoard.Generate()
        game.firstset = 0
        game.hod = game.HOD_NONE

        pygame.draw.rect(game.screen, color.blue_dark,
            (game.pos_myBoard.x, game.pos_myBoard.y, 
            game.myBoard._size * game.cellSize,
            game.myBoard._size * game.cellSize))

        pygame.draw.rect(game.screen, color.blue_dark,
            (game.pos_hisBoard.x, game.pos_hisBoard.y, 
            game.hisBoard._size * game.cellSize,
            game.hisBoard._size * game.cellSize))

        game.draw_hash(game.myBoard, game.pos_myBoard)
        game.draw_hash(game.hisBoard, game.pos_hisBoard)

        pygame.display.update()


        while not finished:
            #act = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #act = 
                    game.mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    game.key_event(event)
                    #act = True

            if game.firstset >= 21:
                if game.myBoard.AllShipsDestroyed():
                    game.lose()
                    return
                if game.hisBoard.AllShipsDestroyed():
                    game.win()
                    return
            
            #if act:
                # game.screen.fill(color.gray)
            game.draw_cells()
            pygame.display.update()

            game.clock.tick(game.FPS)


    @classmethod
    def draw_cells(cls, unhide=True):
        px = game.cellSize

        for i in range(gameBoard._size):
            for j in range(gameBoard._size):
                thiscolor = color.blue_dark
                if game.myBoard.getCell(i, j) == CellState.Deck:
                    if unhide:
                        thiscolor = color.orange
                    else:
                        thiscolor = color.blue_dark
                elif game.myBoard.getCell(i, j) == CellState.Empty:
                    thiscolor = color.blue_dark
                elif game.myBoard.getCell(i, j) == CellState.HitDeck:
                    thiscolor = color.red
                elif game.myBoard.getCell(i, j) == CellState.Miss:
                    thiscolor = color.blue_ligth

                pygame.draw.rect(game.screen, thiscolor,
                            (game.pos_myBoard.x + i * px, game.pos_myBoard.y + j *px, px, px))

                if game.hisBoard.getCell(i, j) == CellState.Deck:
                    if unhide:
                        thiscolor = color.orange
                    else:
                        thiscolor = color.blue_dark
                elif game.hisBoard.getCell(i, j) == CellState.Empty:
                    thiscolor = color.blue_dark
                elif game.hisBoard.getCell(i, j) == CellState.HitDeck:
                    thiscolor = color.red
                elif game.hisBoard.getCell(i, j) == CellState.Miss:
                    thiscolor = color.blue_ligth

                pygame.draw.rect(game.screen, thiscolor,
                            (game.pos_hisBoard.x + i * px, game.pos_hisBoard.y + j *px, px, px))

        game.draw_hash(game.myBoard,game.pos_myBoard)
        game.draw_hash(game.hisBoard,game.pos_hisBoard)

    @classmethod
    def draw_hash(cls, board, boardpos):
        for i in range(board._size + 1):
            px = game.cellSize
            si = board._size
            x = boardpos.x
            y = boardpos.y
            pygame.draw.line(game.screen, color.black, (x + i * px, y + 0), (x + i *px, y + si * px))
            pygame.draw.line(game.screen, color.black, (x + 0, y + i * px), (x + si * px, y + i * px))

    @classmethod
    def attack_him(cls, nx, ny):
        if cls.hisBoard.getCell(ny, nx) == CellState.HitDeck or cls.hisBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.hisBoard.Shoot(nx, ny)

    @classmethod
    def attack_me(cls, nx, ny):
        if cls.myBoard.getCell(ny, nx) == CellState.HitDeck or cls.myBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.myBoard.Shoot(nx, ny)

    @classmethod
    def mouse_event(cls, event):
        pos = pair(event.pos)
        if pos.x >= game.pos_hisBoard.x \
            and pos.x <= game.hisBoard._size * game.cellSize + game.pos_hisBoard.x \
            and pos.y >= game.pos_hisBoard.y \
            and pos.y <= game.hisBoard._size * game.cellSize + game.pos_hisBoard.y :

            pos.x-=game.pos_hisBoard.x
            pos.y-=game.pos_hisBoard.y
            return game.pole_event(pos.x//game.cellSize, pos.y//game.cellSize, 2)
            
            
        elif pos.x >= game.pos_myBoard.x and \
            pos.x <= game.myBoard._size * game.cellSize + game.pos_myBoard.x \
            and pos.y >= game.pos_myBoard.y \
            and pos.y <= game.myBoard._size * game.cellSize + game.pos_myBoard.y :
            
            pos.x-=game.pos_myBoard.x
            pos.y-=game.pos_myBoard.y
            return game.pole_event(pos.x//game.cellSize, pos.y//game.cellSize, 1)
             

        return True
    
    @classmethod
    def pole_event(cls, y, x, sender): #pboxClick
        if game.checkWin():
            return True
        if game.firstset < 21:
            game.prepare(x, y, sender)
            return True
        elif game.getHod() == game.HOD_MY:
            if sender == 2:
                if not game.attack_him(x,y):
                    game.setLabel("Ход вторго игрока")
                    game.setHod(game.HOD_HIS)
                    return True
            else:
                return False
        elif game.getHod() == game.HOD_HIS:
            if sender == 1:
                if not game.attack_me(x,y):
                    game.setLabel("Ход первого игрока")
                    game.setHod(game.HOD_MY)
                    return True
            else:
                return False
        if game.checkWin():
            return True 
        return False

    @classmethod
    def prepare(cls,msx,msy,sender):
        if game.firstset < 10:
            if sender == 1:
                if game.myBoard.PvP(msx,msy,game.rank,game.hori,game.firstset):
                    game.firstset += 1
                    #drawCells(1)
        if game.firstset == 10:
            MessageBox.Show("Передайте поле сопернику")
            game.firstset+=1 
            return
        if game.firstset < 21 and game.firstset >= 10:
            if sender == 2:
                if game.hisBoard.PvP(msx,msy,game.rank,game.hori,game.firstset):
                    game.firstset += 1
                    # drawCells(2)
        if game.firstset >= 21:
            MessageBox.Show("Поле готово. Начинайте партию")
            game.setHod(game.HOD_MY) # FIXME

    rank = 0
    hori = 0

    @classmethod
    def key_event(cls, event):
        if event.unicode == '1':
            game.rank = 1
        elif event.unicode == '2':
            game.rank = 2
        elif event.unicode == '3':
            game.rank = 3
        elif event.unicode == '4':
            game.rank = 4
        elif event.unicode == '5':
            game.hori = 1 - game.hori

    @classmethod
    def setLabel(cls, str):
        print(str)
        # FIXME

    HOD_NONE = 0
    HOD_MY = 1
    HOD_HIS = 2
    hod = HOD_NONE
    @classmethod
    def setHod(cls, ipt):
        game.hod = ipt
    @classmethod
    def getHod(cls):
        return game.hod
    
    @classmethod
    def checkWin(cls): # FIXME
        if  game.myBoard.AllShipsDestroyed() or game.myBoard.AllShipsDestroyed():
            return True
        return False
    
    def win():
        print("WIN")

    def lose():
        print("LOSE")

if __name__ == "__main__":
    game.run()