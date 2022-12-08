from SB_cell import GameBoardCell
from SB_cell import CellState
from SB_ship import Ship
from SB_ship import ShipState


class Ship_set_result:
    OK = 0
    INCORRECT = 1
    OUT_OF_POLE = 2
    OVERCOUNT = 3
    CANT_SET = 4


class GameBoard:
    _size = 10  # размер игорового поля
    _4DeckShipCount = 1  # число 4-х палубных
    _3DeckShipCount = 2  # число 3-х палубных
    _2DeckShipCount = 3  # число 2-х палубных
    _1DeckShipCount = 4  # число 1-х палубных

    # число всех кораблей
    _shipsCount = \
        _4DeckShipCount + \
        _3DeckShipCount + \
        _2DeckShipCount + \
        _1DeckShipCount

    _shipsCountAll = 2 * _shipsCount + 1

    pos = None  # положение на экране

    def __init__(self, sener):
        self.senderName = sener  # поле игрока или противника
        self.Generate()

    def Generate(self):
        self._ships = [Ship() for _ in range(self._shipsCount)]
        self._cells = [[GameBoardCell()
                       for _ in range(self._size)]
                       for __ in range(self._size)]
        self.count = 0
        self.count_of_ships = [4, 3, 2, 1]
        self.hidden = True
        for i in range(self._size):
            for j in range(self._size):
                self._cells[i][j].SetState(CellState.EMPTY)

    def getCell(self, i, j):
        if not self.hidden:
            return self._cells[i][j].GetState()
        else:
            state = self._cells[i][j].GetState()
            if state == CellState.DECK:
                return CellState.EMPTY
            else:
                return state

    def getShipState(self, i, j):
        for k in range(len(self._ships)):
            if self._ships[k].isOn(i, j):
                return self._ships[k].GetState()
        return ShipState.SAFE

    def try_set_ship(self, x, y, r, h, idx):
        if r < 1 or r > 4 or h > 1 or h < 0:
            return Ship_set_result.INCORRECT
        elif (x + (r if h else 0) - 1) >= self._size \
                or (y + (0 if h else r) - 1) >= self._size \
                or x < 0 or y < 0:
            return Ship_set_result.OUT_OF_POLE
        elif not self.check_counter(r):
            return Ship_set_result.OVERCOUNT
        else:
            if not self._ships[idx % 10].Create(self, r, x, y, h):
                return Ship_set_result.CANT_SET
            else:
                self.change_counter(r)
                return Ship_set_result.OK

    def setPos(self, xy):
        self.pos = xy

    def GetCount(self):
        return self._size**2

    def GetSize(self):
        return self._size

    # функция - выстрел в игрове поле
    def Shoot(self, x, y):
        # просмотрим все корабли
        for i in range(self._shipsCount):
            if self._ships[i].TryHit(x, y):
                # если попадаем - стреляем по кораблю
                self._ships[i].Shoot(self, x, y)
                self.setMissDiag(x, y)
                return True
            else:
                # иначе засчитываем промах
                self._cells[x][y].SetState(CellState.MISS)
        return False

    # отметить клетки, где точно нет кораблей (по диагонали от палубы)
    def setMissDiag(self, x, y):
        if x - 1 >= 0:
            if y - 1 >= 0:
                self.SetState(x - 1, y - 1, CellState.MISS)
            if y + 1 < self._size:
                self.SetState(x - 1, y + 1, CellState.MISS)
        if x + 1 < self._size:
            if y - 1 >= 0:
                self.SetState(x + 1, y - 1, CellState.MISS)
            if y + 1 < self._size:
                self.SetState(x + 1, y + 1, CellState.MISS)

    # обход всех кораблей
    def AllShipsDestroyed(self):
        for i in range(self._shipsCount):
            if self._ships[i].GetState() != ShipState.DESTROYED:
                return False  # если хотя бы один не уничтожен, вернем false
        return True

    # функция проверки возможности установки корабля
    def check_counter(self, size):
        return self.count_of_ships[size - 1] != 0

    def change_counter(self, size):
        self.count_of_ships[size - 1] -= 1

    # функция установки статуса клетки игровго поля
    def SetState(self, x, y, state):
        self._cells[x][y].SetState(state)

    # функция возвращает является ли клетка палубой
    def IsDeck(self, x, y):
        return self._cells[x][y].GetState() == CellState.DECK \
            or self._cells[x][y].GetState() == CellState.HIT_DECK

    def hide(self):
        self.hidden = True

    def unhide(self):
        self.hidden = False


class GameTable:
    _size = GameBoard._size
    _shipsCountAll = GameBoard._shipsCount + 1

    pos = None  # положение на экране

    def __init__(self, sener):
        self.senderName = sener
        self.Generate()

    def Generate(self):
        self._cells = [[GameBoardCell()
                       for _ in range(self._size)]
                       for __ in range(self._size)]
        for i in range(self._size):
            for j in range(self._size):
                self._cells[i][j].SetState(CellState.EMPTY)

    def setPos(self, xy):
        self.pos = xy

    def getCell(self, i, j):
        return self._cells[i][j].GetState()

    def SetState(self, x, y, state):
        self._cells[x][y].SetState(state)

    def kill(self, x, y, xy=[[-1, -1]]):
        self.SetState(x, y, CellState.HIT_DECK)
        for c in xy:
            if x == c[0] and y == c[1]:
                return
        for i in range(max(x - 1, 0), min(x + 2, self._size)):
            for j in range(max(y - 1, 0), min(y + 2, self._size)):
                if self.getCell(i, j) == CellState.HIT_DECK:
                    self.kill(i, j, xy + [[x, y]])
                elif self.getCell(i, j) == CellState.EMPTY:
                    self.SetState(i, j, CellState.MISS)

    def damage(self, x, y):
        self.SetState(x, y, CellState.HIT_DECK)
        self.setMissDiag(x, y)

    # отметить клетки, где точно нет кораблей (по диагонали от палубы)
    def setMissDiag(self, x, y):
        if x - 1 >= 0:
            if y - 1 >= 0:
                self.SetState(x - 1, y - 1, CellState.MISS)
            if y + 1 < self._size:
                self.SetState(x - 1, y + 1, CellState.MISS)
        if x + 1 < self._size:
            if y - 1 >= 0:
                self.SetState(x + 1, y - 1, CellState.MISS)
            if y + 1 < self._size:
                self.SetState(x + 1, y + 1, CellState.MISS)


if __name__ == "__main__":
    print("This module is not for direct call!")
