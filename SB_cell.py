class CellState:
    EMPTY = 0
    DECK = 1
    MISS = 2
    HIT_DECK = 3


class GameBoardCell:
    x = -1
    y = -1
    state = -1

    def __init__(self, x0=0, y0=0, state0=CellState.EMPTY):
        self.x = x0
        self.y = y0
        self.state = state0

    def SetX(self, x0):
        self.x = x0

    def SetY(self, y0):
        self.y = y0

    def SetState(self, state0):
        self.state = state0

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y

    def GetState(self):
        return self.state

    def TryHit(self, x0, y0):
        return self.x == x0 and self.y == y0 \
            and self.state != CellState.HIT_DECK \
            and self.state != CellState.MISS


if __name__ == "__main__":
    print("This module is not for direct call!")
