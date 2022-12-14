from SB_cell import GameBoardCell
from SB_cell import CellState


class ShipState:
    DESTROYED = 0
    HITTED = 1
    SAFE = 2


class Ship:
    def __init__(self):
        self._size = -1

    def Create(self, gameBoard, size, x, y, is_horizontal):
        self._size = size
        self._cells = [GameBoardCell() for _ in range(size)]
        # проверяем, не заполненны ли клетки
        # вокруг выбранного расположения корабля
        if is_horizontal:
            for j in range(
                    max(0, y - 1),
                    min(y + 1 + 1, gameBoard.GetSize())):
                for i in range(
                        max(0, x - 1),
                        min(x + size + 1, gameBoard.GetSize())):
                    if gameBoard.IsDeck(i, j):
                        return False
        else:
            for j in range(
                    max(0, x - 1),
                    min(x + 1 + 1, gameBoard.GetSize())):
                for i in range(
                        max(0, y - 1),
                        min(y + size + 1, gameBoard.GetSize())):
                    if gameBoard.IsDeck(j, i):
                        return False
        # если не заполнены
        for i in range(size):
            if is_horizontal:
                self._cells[i].SetX(x + i)
                self._cells[i].SetY(y)
                gameBoard.SetState(x + i, y, CellState.DECK)
            else:
                self._cells[i].SetX(x)
                self._cells[i].SetY(y + i)
                gameBoard.SetState(x, y + i, CellState.DECK)

        return True

    def GetState(self):
        # считаем число попаданий
        hitCount = 0
        for i in range(self._size):
            if self._cells[i].GetState() == CellState.HIT_DECK:
                hitCount += 1

        # сверяем число попаданий с числом палуб
        if hitCount == 0:  # если не попали - корабль цел
            self._state = ShipState.SAFE
        elif hitCount < self._size:
            # если попали, но меньше раз, чем число палуб, то ранен
            self._state = ShipState.HITTED
        else:
            self._state = ShipState.DESTROYED  # иначе - уничтожен

        return self._state

    # функция выстрела по корабрю, возвращает состояние корябля после выстрела
    def Shoot(self, gameBoard, x, y):
        for i in range(self._size):
            if self._cells[i].TryHit(x, y):
                self._cells[i].SetState(CellState.HIT_DECK)
                gameBoard.SetState(x, y, CellState.HIT_DECK)
                break
        if self.GetState() == ShipState.DESTROYED:
            for i in range(self._size):
                localX = self._cells[i].GetX()
                localY = self._cells[i].GetY()

                if localX - 1 >= 0 and localY - 1 >= 0 \
                        and not gameBoard.IsDeck(localX - 1, localY - 1):
                    gameBoard.SetState(localX - 1, localY - 1, CellState.MISS)

                if localX - 1 >= 0 \
                        and not gameBoard.IsDeck(localX - 1, localY):
                    gameBoard.SetState(localX - 1, localY, CellState.MISS)

                if localX - 1 >= 0 and localY + 1 < gameBoard.GetSize() \
                        and not gameBoard.IsDeck(localX - 1, localY + 1):
                    gameBoard.SetState(localX - 1, localY + 1, CellState.MISS)
                # ===
                if localY - 1 >= 0 \
                        and not gameBoard.IsDeck(localX, localY - 1):
                    gameBoard.SetState(localX, localY - 1, CellState.MISS)

                if localY + 1 < gameBoard.GetSize()\
                        and not gameBoard.IsDeck(localX, localY + 1):
                    gameBoard.SetState(localX, localY + 1, CellState.MISS)
                # ===
                if localX + 1 < gameBoard.GetSize() and localY - 1 >= 0 \
                        and not gameBoard.IsDeck(localX + 1, localY - 1):
                    gameBoard.SetState(localX + 1, localY - 1, CellState.MISS)
                if localX + 1 < gameBoard.GetSize() \
                        and not gameBoard.IsDeck(localX + 1, localY):
                    gameBoard.SetState(localX + 1, localY, CellState.MISS)
                if localX + 1 < gameBoard.GetSize() \
                        and localY + 1 < gameBoard.GetSize() \
                        and not gameBoard.IsDeck(localX + 1, localY + 1):
                    gameBoard.SetState(localX + 1, localY + 1, CellState.MISS)

    def TryHit(self, x, y):
        for i in range(self._size):
            if self._cells[i].TryHit(x, y):
                return True
        return False

    def isOn(self, x, y):
        for i in range(len(self._cells)):
            if self._cells[i].GetX() == x and self._cells[i].GetY() == y:
                return True
        return False
        """for c in self._cells:  # doesn't work
            if c.GetX() == x and c.GetY() == y:
                return True
        return False"""


if __name__ == "__main__":
    print("This module is not for direct call!")
