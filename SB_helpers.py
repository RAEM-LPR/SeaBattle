class SB_strings:
    pr_incorrect = "Вы ввели некорректные координаты корабля"
    pr_out = "Вы отметили координаты корабля так,\
    что он вышел за пределы игрового поля"
    pr_ovf = "Вы привысили допустимый лимит кораблей данного типа"
    pr_cant = "Вы отметили  координаты корабля так, что его нельзя установить"
    motion2 = "Ход вторго игрока"
    motion1 = "Ход первого игрока"
    motionm = "Ваш ход"
    motionh = "Ход вашего противника"
    motionw = "Ожидание результата"
    waittoset = "Ваш соперник не готов"
    prepare10 = "Передайте поле сопернику"
    prepare_done = "Поле готово. Начинайте партию"
    prepare_done1 = "Поле готово. Начинайте партию. Ход первого игрока"
    prepare_done2 = "Поле готово. Начинайте партию. Ход первого игрока"
    letsbegin = "Расставьте свои корабли"
    win = "Первый игрок выиграл"
    lose = "Второй игрок выиграл"
    win_link = "Вы выиграли"
    lose_link = "Вы проиграли"


class SB_colors:
    gray = 0xF0F0F0
    blue_dark = 0x00008B
    blue_ligth = 0x5F9EA0
    orange = 0xFF8C00
    red = 0xFF0000
    black = 0x000000


class SB_pair:
    x = -1
    y = -1

    def __init__(self, r):
        self.x = r[0]
        self.y = r[1]


if __name__ == "__main__":
    print("This module is not for direct call!")
