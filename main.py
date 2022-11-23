import pubnub
import pygame


class CellState:
    Empty = 0
    Deck = 1
    Miss = 2
    HitDeck = 3

class ShipState:
    Destroyed = 0
    ShipHit = 1
    Safe = 2

class ShipCounter:
    Four_deck = 1
    Three_deck = 2
    Two_deck = 3
    One_deck = 4

class color:
    gray = 0xF0F0F0
    blue_dark = 0x00008B
    blue_ligth = 0x5F9EA0
    orange = 0xFF8C00
    red = 0xFF0000
    black = 0x000000


class pair:
    x = -1
    y = -1
    def __init__(self, r):
        self.x = r[0]
        self.y = r[1]

class MessageBox:
    @classmethod
    def Show(cls, str):
        print(str)

class GameBoardCell:
    x = -1
    y = -1
    state = -1
    def __init__(self, x0=0,y0=0,state0=CellState.Empty):
        self.x = x0
        self.y = y0
        self.state = state0
    def set_x(self, x0):
        self.x = x0
    def set_y(self, y0):
        self.y = y0
    def set_state(self, state0):
        self.state = state0
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_state(self):
        return self.state
    def try_hit(self, x0, y0):
        return self.x == x0 and self.y == y0 and self.state != CellState.HitDeck		

class Ship:
    _cells = []
    _state = -1
    _size = -1

    def __init__(self):
        pass
    #вернуть create в конструктор + бросать исключения (опредилить свой класс)
    def create(self, gameBoard, size, x ,y, is_horizontal): #gameBoard, int size, int x, int y, bool horizontal
        self._size = size
        for i in range(size):
            self._cells.append(GameBoardCell())
        not_filled = True # заполненно ли что-то из выбранного расположения корабля
        # проверяем, не заполненны ли клетки вокруг выбранного расположения корабля
        try: # FIXME zip loop
            if is_horizontal: 
                for j in range(max(0, y - 1),min(y + 1 + 1, gameBoard.GetSize())):
                    for i in range(max(0, x - 1), min(x + size + 1, gameBoard.GetSize())):
                        if gameBoard.IsDeck(i, j):
                            not_filled = False
                            raise Exception()
            else:
                for j in range(max(0, x - 1),min(y + x + 1, gameBoard.GetSize())):
                    for i in range(max(0, y - 1), min(y + size + 1, gameBoard.GetSize())):
                        if gameBoard.IsDeck(j, i):
                            not_filled = False
                            raise Exception()
        except: 
            pass

        if not_filled:
            for i in range(size):
                if is_horizontal:
                    self._cells[i].SetX(x + i)
                    self._cells[i].SetY(y)
                    gameBoard.SetState(x + i, y, CellState.Deck)
                else:
                    self._cells[i].SetX(x)
                    self._cells[i].SetY(y + i)
                    gameBoard.SetState(x, y + i, CellState.Deck)
        
        return not_filled

    def GetState(self):
        #считаем число попаданий
        hitCount = 0
        for i in range (self._size):
            if self._cells[i].GetState() == CellState.HitDeck:
                hitCount += 1

        # сверяем число попаданий с числом палуб
        if hitCount == 0: # если не попали - корабль цел
            self._state = ShipState.Safe
        elif hitCount < self._size: # если попали, но меньше раз, чем число палуб, то ранен
            self._state = ShipState.ShipHit
        else:
            self._state = ShipState.Destroyed # иначе уничтожен

        return self._state

    # функция выстрела по корабрю, возвращает состояние корябля после выстрела
    def Shoot(self, gameBoard, x, y):
        for i in range (self._size):
            if self._cells[i].TryHit(x, y):
                self._cells[i].SetState(CellState.HitDeck);
                gameBoard.SetState(x, y, CellState.HitDeck);
                break
        if self.GetState() == ShipState.Destroyed:
            for i in range (self._size):
                localX = self._cells[i].GetX()
                localY = self._cells[i].GetY()

                if localX - 1 >= 0 and localY - 1 >= 0 and not gameBoard.IsDeck(localX - 1, localY - 1):
                    gameBoard.SetState(localX - 1, localY - 1, CellState.Miss)
                if localX - 1 >= 0 and not gameBoard.IsDeck(localX - 1, localY):
                    gameBoard.SetState(localX - 1, localY, CellState.Miss)
                if localX - 1 >= 0 and localY + 1 < gameBoard.GetSize() and not gameBoard.IsDeck(localX - 1, localY + 1):
                    gameBoard.SetState(localX - 1, localY + 1, CellState.Miss)

                if localY - 1 >= 0 and not gameBoard.IsDeck(localX, localY - 1):
                    gameBoard.SetState(localX, localY - 1, CellState.Miss)
                if localY + 1 < gameBoard.GetSize() and not gameBoard.IsDeck(localX, localY + 1):
                    gameBoard.SetState(localX, localY + 1, CellState.Miss)

                if localX + 1 < gameBoard.GetSize() and localY - 1 >= 0 and not gameBoard.IsDeck(localX + 1, localY - 1):
                    gameBoard.SetState(localX + 1, localY - 1, CellState.Miss)
                if localX + 1 < gameBoard.GetSize() and not gameBoard.IsDeck(localX + 1, localY):
                    gameBoard.SetState(localX + 1, localY, CellState.Miss)
                if localX + 1 < gameBoard.GetSize() and localY + 1 < gameBoard.GetSize() and not gameBoard.IsDeck(localX + 1, localY + 1):
                    gameBoard.SetState(localX + 1, localY + 1, CellState.Miss)
    
    def TryHit(self, x, y):
        for i in range(self._size):
            if self._cells[i].TryHit(x, y):
                return True
        return False
    

class gameBoard:
    _size = 10; # размер игорового поля
    _4DeckShipCount = 1; # число 4-х палубных
    _3DeckShipCount = 2; # число 3-х палубных
    _2DeckShipCount = 3; # число 2-х палубных
    _1DeckShipCount = 4; # число 1-х палубных
    _shipsCount = _4DeckShipCount + _3DeckShipCount + _2DeckShipCount + _1DeckShipCount; # число кораблей
    _cells = [[]] # клетки игрового поля
    _ships = [] # корабли
    count = 0
    count_of_ships = (4, 3, 2, 1)

    def __init__(self, x=0,y=0,state=0):
        self._ships = [Ship() for _ in range (self._shipsCount + 1)]
        self._cells = [[GameBoardCell() for _ in range(self._size)] for __ in range(self._size)]

        #for i in range(self._size):
        #    self._cells.append([GameBoardCell() for _ in range(self._size)])

    def getCell(self, i, j):
        return self._cells[i][j].GetState()

    def Generate(self):
        for i in range(self._size):
            for j in range(self._size):
                self.cells[i][j].SetState(CellState.Empty) 

    def PvP(self, gameBoard, x, y, r, h, idx):
        idx %= 10

        if r < 1 or r > 4 or h > 1 or h < 0:      
            MessageBox.Show("\nВы ввели некорректные координаты корабля\n")    
        elif (x + r * h - 1) > 9 or (y + (r if h == 0 else 0) - 1) > 9 or x < 0 or y < 0:      
            MessageBox.Show("\nВы отметили координаты корабля так, что он вышел за пределы игрового поля\n")
        elif (not gameBoard.check_counter(r)):    
            MessageBox.Show("Вы привысили допустимый лимит кораблей данного типа\n");    
        else:
            idx+=1
            if (not self._ships[idx].Create(self, r, x, y, h != 0 )): # FIXME Create(this, 
                MessageBox.Show("\nВы отметили  координаты корабля так, что его нельзя установить, введите данные заново\n\n");
                idx-=1 #FIXME error?
            else:
                gameBoard.change_counter(r)
                return True
        return False
    
    def GetCount(self):
        return self._size**2

    def GetSize(self):
        return self._size

    #функция - выстрел в игрове поле
    def Shoot(self, x, y):
        #просмотрим все корабли
        for i in range(self._shipsCount):
            if self._ships[i].TryHit(x, y):
                # если попадаем - стреляем по кораблю
                self._ships[i].Shoot(self, x, y); # FIXME (this, 
                return True
            else:
                # иначе засчитываем промах
                self._cells[y][x].SetState(CellState.Miss)
        return False

    def AllShipsDestroyed(self):
	#обход всех кораблей
        for i in range(self._shipsCount):
            if self._ships[i].GetState() != ShipState.Destroyed: # если хотя бы один не уничтожен, вернем false
                return False # если хотя бы один не уничтожен, вернем false
        return True

    #функция проверки возможности установки корабля
    def check_counter(self, size):
        return self.count_of_ships[size - 1] != 0

    def change_counter(self, size):
        self.count_of_ships[size - 1]-=1


class game:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 500
    FPS = 10
    pos_myBoard = pair((40,25))
    pos_hisBoard = pair((560,25))
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
            act = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    act = game.mouse_event(event)
                elif event.type == pygame.KEYDOWN:
                    game.key_event(event)
                    act = True

            if game.myBoard.AllShipsDestroyed():
                ...
            if game.hisBoard.AllShipsDestroyed():
                ...
            
            if act:
                # game.screen.fill(color.gray)
                game.draw_cells()
                game.clock.tick(game.FPS)
                pygame.display.update()


    @classmethod
    def draw_cells(cls):
        game.screen

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
        if cls.hisBoard.getCell(ny, nx) == CellState.HitDeck | cls.hisBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.hisBoard.Shoot(nx, ny)

    @classmethod
    def attack_me(cls, nx, ny):
        if cls.myBoard.getCell(ny, nx) == CellState.HitDeck | cls.myBoard.getCell(ny, nx) == CellState.Miss:
            return True
        return cls.myBoard.Shoot(nx, ny)

    @classmethod
    def mouse_event(cls, event):
        pos = pair(event.pos)
        if pos.x > game.pos_hisBoard.x \
            and pos.x < game.hisBoard._size * game.cellSize + game.pos_hisBoard.x \
            and pos.y > game.pos_hisBoard.y \
            and pos.y < game.hisBoard._size * game.cellSize + game.pos_hisBoard.y :

            pos.x-=game.pos_hisBoard.x
            pos.y-=game.pos_hisBoard.y
            return game.pole_event(pos.x//game.cellSize,pos.y//game.cellSize, 2)
            
            
        elif pos.x > game.pos_myBoard.x and \
            pos.x < game.myBoard._size * game.cellSize + game.pos_myBoard.x \
            and pos.y > game.pos_myBoard.y \
            and pos.y < game.myBoard._size * game.cellSize + game.pos_myBoard.y :
            
            pos.x-=game.pos_myBoard.x
            pos.y-=game.pos_myBoard.y
            return game.pole_event(pos.x//game.cellSize,pos.y//game.cellSize, 1)
             

        return True
    
    @classmethod
    def pole_event(cls, x, y, sender): #pboxClick
        if game.checkWin():
            return True
        if game.firstset < 21:
            game.prepare()
            return True
        elif game.getHod() == game.HOD_MY:
            if sender == 2:
                if not game.attack_him(x,y):
                    game.setLabel("Ход вторго игрока")
                    return True
            else:
                return False
        elif game.getHod() == game.HOD_HIS:
            if sender == 1:
                if not game.attack_me(x,y):
                    game.setLabel("Ход первого игрока")
                    return True
            else:
                return False
        if game.checkWin():
            return True 
        return False

    @classmethod
    def prepare(cls):
        ...

    @classmethod
    def key_event(cls, event):
        if event.unicode == '1':
            ...

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

game.run()