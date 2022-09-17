import sys
from random import randint
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtCore import Qt


class Main(QWidget):
    def __init__(self, a=10):
        super().__init__()
        self.a, self.m, self.bombs = a, a ** 2 // 10, {}
        self.w, self.h = self.size().width(), self.size().height()
        self.ca, self.fiv, self.flag = 10, [], False
        self.win = False
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Sapper')
        self.cbtn = QPushButton('CLEAR', self)
        self.cbtn.setStyleSheet("background-color: red")
        self.cbtn.clicked.connect(self.clear)
        self.modeb = QPushButton('Step\nmode', self)
        self.modeb.clicked.connect(self.mode)
        self.defuse_lamp = QPushButton('defuse\nlamp', self)
        self.init_field(self.a)

    def init_field(self, a=0):
        self.win, self.flag = False, False
        self.bombs.clear()
        if a > 2:
            self.a, self.m = a, a ** 2 // 10
            self.ca = ((self.w - 10) / (self.a + 2) if self.w < self.h else (self.h - 10) / (self.a + 2)) * 0.8
        self.fiv = [[QPushButton('?', self) for i in range(self.a)] for _ in range(self.a)]
        self.defuse_lamp.setStyleSheet("background-color: lightGray")
        for y in range(self.a):
            for x in range(self.a):
                self.fiv[y][x].setAccessibleName(f'{x}#{y}')
                self.fiv[y][x].clicked.connect(self.step)
                self.fiv[y][x].show()
        self.resizeEvent(None)

    def set_bombs(self, px, py):
        while len(self.bombs.keys()) < self.m:
            x, y = randint(0, self.a - 1), randint(0, self.a - 1)
            if (x, y) not in self.bombs.keys() and x != px and y != py:
                self.bombs[(x, y)] = 'U'
        self.set_cell(px, py, 'S')

    def resizeEvent(self, event):
        nkw, nkh = self.size().width() / self.w, self.size().height() / self.h
        self.cbtn.setGeometry(int(10 * nkw), int(400 * nkh), int(620 * nkw), int(60 * nkh))
        self.modeb.setGeometry(int(550 * nkw), int(100 * nkh), int(80 * nkw), int(80 * nkh))
        self.defuse_lamp.setGeometry(int(550 * nkw), int(190 * nkh), int(80 * nkw), int(80 * nkh))
        for y in range(self.a):
            for x in range(self.a):
                a1, a2 = int((x + 1) * self.ca * 1.05 * nkw), int((y + 1) * self.ca * 1.05 * nkh)
                self.fiv[y][x].setGeometry(a1, a2, int(self.ca * 0.95 * nkw), int(self.ca * 0.95 * nkh))
                self.fiv[y][x].setFont(QFont("Times", int(8 * (nkw + nkh))))
        self.cbtn.setFont(QFont("Times", int(9 * (nkw + nkh))))
        self.modeb.setFont(QFont("Times", int(8 * (nkw + nkh))))
        self.defuse_lamp.setFont(QFont("Times", int(8 * (nkw + nkh))))

    def clear(self):
        self.init_field(self.a)

    def mode(self):
        if self.modeb.text() == 'Flag\nmode':
            self.modeb.setText('Step\nmode')
            self.modeb.setStyleSheet("background-color: lightGray")
        else:
            self.modeb.setText('Flag\nmode')
            if self.m <= 0:
                self.modeb.setStyleSheet("background-color: red")
            else:
                self.modeb.setStyleSheet("background-color: green")

    def step(self):
        if self.win != -1:
            button = QApplication.instance().sender()
            x, y = map(int, button.accessibleName().split('#'))
            if not self.flag and 'Flag' not in self.modeb.text():
                self.flag = True
                self.set_bombs(x, y)
            if 'Flag' in self.modeb.text():
                rez = self.set_cell(x, y, 'F')
                if self.m == 0:
                    self.modeb.setStyleSheet("background-color: red")
                else:
                    self.modeb.setStyleSheet("background-color: green")
            else:
                rez = self.set_cell(x, y, 'S')
            if self.check_win():
                self.win = 1
                self.defuse_lamp.setStyleSheet("background-color: green")
            if 'BOOM!' in rez and self.win == 0:
                self.win = -1
                self.defuse_lamp.setStyleSheet("background-color: red")
            elif 'BOOM!' in rez and self.win == 1:
                self.fiv[y][x].setStyleSheet("background-color: red")

    def find_bombs(self, x, y):
        points, stp = [], 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i in range(self.a) and j in range(self.a ):
                    if (j, i) in self.bombs.keys():
                        stp += 1
                        flag = 1
                    else:
                        points.append((j, i))
        return [stp, points]

    def check_win(self):
        for i in self.bombs.keys():
            if "U" == self.bombs[i]:
                return False
        return True

    def set_cell(self, x, y, tp, flag=5):
        if x not in range(self.a) or y not in range(self.a):
            return 'ERROR: CELL NOT IN FIELD'
        elif tp.upper() == 'F' and self.m == 0 and self.fiv[y][x].text() == '?':
            return 'ERROR: YOU HAVE 0 FLAGS'
        if tp.upper() == 'F':
            if self.fiv[y][x].text() == '?':
                self.fiv[y][x].setText('F')
                self.fiv[y][x].setStyleSheet("background-color: blue")
                self.m -= 1
                if (x, y) in self.bombs.keys():
                    self.bombs[(x, y)] = 'F'
                return 'SUCCESSFUL'
            elif self.fiv[y][x].text() == 'F':
                self.fiv[y][x].setText('?')
                self.fiv[y][x].setStyleSheet("background-color: lightGray")
                self.m += 1
                if (x, y) in self.bombs.keys():
                    self.bombs[(x, y)] = 'U'
                return 'SUCCESSFUL'
            else:
                return 'ERROR: CELL NOT UNDER FLAG'
        elif tp.upper() == 'S':
            if self.fiv[y][x].text() == 'F':
                self.fiv[y][x].setText('?')
                self.fiv[y][x].setStyleSheet("background-color: lightGray")
                self.m += 1
            if (x, y) in self.bombs.keys():
                return 'BOOM!'
            else:
                stp, poi = list(self.find_bombs(x, y))
                self.fiv[y][x].setText(str(stp))
                if not stp:
                    self.fiv[y][x].setText('')
                if flag and not stp:
                    for po in poi:
                        self.set_cell(po[0], po[1], 'S', flag - 1)
                return 'SUCCESSFUL'


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Windows')
    ex = Main(15)
    palette = QPalette()
    palette.setColor(QPalette.Background, Qt.darkGray)
    ex.setPalette(palette)
    ex.show()
    sys.exit(app.exec())