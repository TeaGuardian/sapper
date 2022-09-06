from random import randint

class Field:
    def __init__(self, x, y, px, py):
        self.x, self.y, self.m = x, y, x * y // 10
        self.fiv = [['?' for i in range(x)] for _ in range(y)]
        self.bombs = {}
        while len(self.bombs.keys()) < self.m:
            x, y = randint(0, self.x - 1), randint(0, self.y - 1)
            if (x, y) not in self.bombs.keys() and x != px and y != py:
                self.bombs[(x, y)] = 'U'
        self.set_cell(px, py, 'S')

    def print_field(self):
        print(f'FLAGS: {self.m}; BOMBS: {len(self.bombs)}')
        for i in self.fiv:
            for j in i:
                print(f' {j} ', end='')
            print('')

    def find_bombs(self, x, y):
        points, stp = [], 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i in range(self.y) and j in range(self.x):
                    if (j, i) in self.bombs.keys():
                        stp += 1
                    else:
                        points.append((j, i))
        return stp, points

    def check_win(self):
        for i in self.bombs.keys():
            if "U" == self.bombs[i]:
                return False
        return True

    def set_cell(self, x, y, tp, flag=4):
        if x not in range(self.x) or y not in range(self.y):
            return 'ERROR: CELL NOT IN FIELD'
        elif tp.upper() == 'F' and self.m == 0:
            return 'ERROR: YOU HAVE 0 FLAGS'
        if tp.upper() == 'F':
            if self.fiv[y][x] == '?':
                self.fiv[y][x] = 'F'
                self.m -= 1
                if (x, y) in self.bombs.keys():
                    self.bombs[(x, y)] = 'F'
                return 'SUCCESSFUL'
            else:
                return 'ERROR: CELL OCCUPIED'
        elif tp.upper() == 'U':
            if self.fiv[y][x] == 'F':
                self.fiv[y][x] = '?'
                self.m += 1
                if (x, y) in self.bombs.keys():
                    self.bombs[(x, y)] = 'U'
                return 'SUCCESSFUL'
            else:
                return 'ERROR: CELL NOT UNDER FLAG'
        elif tp.upper() == 'S':
            if self.fiv[y][x] == '?':
                self.fiv[y][x] = '?'
                self.m += 1
            if (x, y) in self.bombs.keys():
                return 'BOOM!'
            else:
                stp, poi = self.find_bombs(x, y)
                if stp > 0:
                    self.fiv[y][x] = str(stp)
                    return 'SUCCESSFUL'
                self.fiv[y][x] = ' '
                if flag:
                    for po in poi:
                        self.set_cell(po[0], po[1], 'S', flag - 1)


maxx, maxy = map(int, input('введите размеры поля через пробел: ').split())
px, py = map(int, input('введите начальную точку: ').split())
print("вводите ходы в формате Х У ход")
print("ходы: F - поставить флаг; U - снять флаг; S - наступить")
player = Field(maxx, maxy, px, py)
player.print_field()
while True:
    x, y, step = input('введите ход: ').split()
    rez = player.set_cell(int(x), int(y), step)
    print(rez)
    player.print_field()
    if 'BOOM!' in rez:
        break
    if player.check_win():
        print("ВЫ ПОБЕДИЛИ!")
        break