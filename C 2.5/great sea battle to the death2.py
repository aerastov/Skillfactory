from random import randint
import time

clear = "\n" * 5
print("\nПривет! Давай сыграем в морской бой!")
print("Есть два варианта игры - поле 6х6 и 7 кораблей, и поле 10х10 на котором 10 кораблей.")
print("Выиграет сильнейший!")
try:
    size = int(
        input("Выбери размер поля: 6х6 или 10х10 клеток (жми 6, если хочешь маленькое поле, иначе будет 10х10): "))
    if size != 6: size = 10
except ValueError:
    size = 10


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class BoardException(Exception): pass
class BoardWrongShipException(BoardException):
    pass

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow  # координаты носа (x, y)
        self.l = l  # длинна корабля
        self.o = o  # ориентация (0 - горизонтально, 1 - вертикально)
        self.lives = l  # кол-во жизней равно длинне корабля

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, size):
        self.size = size

    @property
    def random_board(self):  # генерим доску с кораблями, пока не будет удачной расстановки
        board = None
        while board is None: board = self.generation_board()
        return board

    def generation_board(self):  # random_place
        # Матрица size * size для каждой доски: (0 пусто; 1 корабль, 2 мимо, 3 ранен)
        if self.size == 10:
            lens = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        else:
            lens = [3, 2, 2, 1, 1, 1, 1]
        self.field = [[0 for j in range(self.size)] for i in range(self.size)]
        self.busy = []  # список занятых ячеек (вокруг кораблей для правильной генерации)
        self.ships = []  # список ячеек занятых самими кораблями

        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 100: return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    self.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        self.begin()  # Очищаем ячейки вокруг кораблей
        return self.field

    def add_ship(self, ship):
        for d in ship.dots:  # ship.dots - список точек проверяемого корабля
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = 2
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def begin(self):
        self.busy = []


class Out_board: # Выводим в консоль обе доски рядом
    def __init__(self, size, board_user, board_comp):
        self.board_comp = board_comp
        self.board_user = board_user
        self.size = size

    def print_board(self):
        print(clear)
        while True:
            if self.size == 10:
                print("        Твое поле боя:", " " * 20, "Поле боя вражеского AI:")
                print(
                    "  \033[4mА  Б  В  Г  Д  Е  Ж  З  И  К\033[0m" + " " * 12 + "\033[4mА  Б  В  Г  Д  Е  Ж  З  И  К\033[0m")
            else:
                print("   Твое поле боя:", " " * 8, "Поле боя вражеского AI:")
                print("  \033[4mА  Б  В  Г  Д  Е\033[0m" + " " * 12 + "\033[4mА  Б  В  Г  Д  Е\033[0m")

            board_user_iter = iter(self.board_user)
            board_comp_iter = iter(self.board_comp)
            for i in range(0, self.size):
                p2 = str("  ".join(map(str, next(board_comp_iter))))
                # p2 = p2.replace("2", "0") # Стираем с доски корабли противника (AI)
                board = str(
                    "|" + "  ".join(
                        map(str, next(board_user_iter))) + "|" + " " * 10 + "|" + p2 + "|")  # Собираем строку
                board = board.replace("1", "*")  # Тут и далее конвертируем цифры в отображаемые элементы
                board = board.replace("0", "·")
                board = board.replace("2", "■")
                board = board.replace("3", "\033[31m\033[5mХ\033[0m")
                # if i == 10: y = str(i)
                # else: y = str(" " + str(i))
                print(str(i) + board + str(i))
            if self.size == 10:
                print("  " + "—" * 28 + " " * 12 + "—" * 28)
            else:
                print("  " + "—" * 16 + " " * 12 + "—" * 16)
            break

class Shot_processing():
    def __init__(self, size, board):
        self.size = size
        self.board = board

    def step_user(self):
        print("Сейчас твой ход! Переключись на русский и жми координаты (пример: А0), можно без пробела!")
        while True:  # Цикл проверки на корректность введеных координат (что не стрельнул в занятую ячейку)
            while True:  # Цикл ввода пользователем координат хода
                user_xy = input("Координаты хода: ")
                user_xy = user_xy.lower()
                for i in range(len(user_xy)):  # Проверим, что там ввел юзер и уберем лишнее
                    if self.size == 6:
                        if user_xy[i] not in "012345абвгде":  # отсеиваем все, кроме верных символов для доски 6х6
                            user_xy = user_xy.replace(user_xy[i], " ")
                    else:
                        if user_xy[i] not in "0123456789абвгдежзик":  # отсеиваем лишнее для доски 10х10
                            user_xy = user_xy.replace(user_xy[i], " ")
                user_xy = user_xy.replace(" ", "")  # теперь удалим пробелы после чистки
                try:
                    if len(user_xy) != 2:  # если осталось не 2 значения, начинаем цикл ввода снова
                        raise ValueError
                except ValueError:
                    print("Введено не две координаты! ( распознано", user_xy, ") Введи букву и цифру!")
                else:
                    x = user_xy[0]
                    y = user_xy[1]
                    if y.isdigit() and not x.isdigit():
                        break  # проверяем, что y-цифра, а х-буква
                    else:
                        x, y = y, x  # Если условие выше неверно, меняем y и х местами
                    try:
                        if y.isdigit() and not x.isdigit():
                            break  # снова проверяем, что y-цифра, а х-буква
                        else:
                            raise ValueError  # итак, если если введено не цифра + буква, или наоборот, начинаем цикл снова
                    except ValueError:
                        print("Ты ввел что-то не то ( распознано", user_xy,
                              ") Надо букву и цифру из тех, что на доске!")
            n = 0
            for i in "абвгдежзик":
                if x == i:
                    x = n
                else:
                    n += 1
            y = int(y)
            try:
                if self.board[y][x] == 0 or self.board[y][x] == 2:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Невозможный ход! Клетка занята! Будь внимательней!")
        return [y, x]

    def step_ai(self, ai_shot):
        self.old_ai_shot = ai_shot
        while True:
            y = randint(0, (self.size - 1))
            x = randint(0, (self.size - 1))
            if self.board[y][x] == 0 or self.board[y][x] == 2: break
            # time.sleep(1)



        return [y, x]

    def result_shot(self, shot):
        self.shot = shot
        y = self.shot[0]
        x = self.shot[1]
        ship = []
        if self.board[y][x] == 2:
            ship.append(3)
            i = x # раз попал, то проверяем убит ли корабль
            while i >= 1: # Проверяем корабль по горизонтали
                i -= 1
                if self.board[y][i] in range(0, 2): break
                else: ship.append(self.board[y][i])
            i = x
            a = 8 if self.size == 10 else 4
            while i <= a:
                i += 1
                if self.board[y][i] in range(0, 2): break
                else: ship.append(self.board[y][i])
            i = y
            while i >= 1: # Проверяем корабль по вертикали
                i -= 1
                if self.board[i][x] in range(0, 2): break
                else: ship.append(self.board[i][x])
            i = y
            a = 8 if self.size == 10 else 4
            while i <= a:
                i += 1
                if self.board[i][x] in range(0, 2): break
                else: ship.append(self.board[i][x])

            print("тест, вычисление корабля: ", ship)
            if len(ship) * 3 == sum(ship): return "убил"
            return "ранил"

        if self.board[self.shot[0]][self.shot[1]] == 0:
            return "мимо"


    def changing_board(self, result):
        self.result = result
        y = self.shot[0]
        x = self.shot[1]
        if self.result == "ранил": self.board[y][x] = 3
        if self.result == "мимо": self.board[y][x] = 1
        if self.result == "убил":
            self.board[y][x] = 3
            i = x
            while i >= 1:  # Проверяем корабль по горизонтали
                i -= 1
                if self.board[y][i] != 3: # Если крестика нет, значит граница корабля, обводим
                    self.board[y][i] = 1
                    if y != 0: self.board[y-1][i] = 1
                    if y != (self.size - 1): self.board[y+1][i] = 1
                    break
                else: # если в левой клетке 3, то корабль это тело горизонтального корабля, ставим * вверху и внизу
                    if y != 0: self.board[y-1][i] = 1
                    if y != (self.size - 1): self.board[y+1][i] = 1
            i = x
            a = 8 if self.size == 10 else 4
            while i <= a:
                i += 1
                if self.board[y][i] != 3: # Если крестика нет, значит граница корабля, обводим
                    self.board[y][i] = 1
                    if y != 0: self.board[y - 1][i] = 1
                    if y != (self.size - 1): self.board[y + 1][i] = 1
                    break
                else: # если в левой клетке 3, то корабль это тело горизонтального корабля, ставим * вверху и внизу
                    if y != 0: self.board[y-1][i] = 1
                    if y != (self.size - 1): self.board[y+1][i] = 1
            i = y
            while i >= 1:  # Проверяем корабль вверх
                i -= 1
                if self.board[i][x] != 3: # Если крестика нет, значит граница корабля, обводим
                    self.board[i][x] = 1
                    if x != 0: self.board[i][x-1] = 1
                    if x != (self.size - 1): self.board[i][x+1] = 1
                    break
                else: # если в верхней клетке 3, то корабль это тело горизонтального корабля, ставим * вверху и внизу
                    if x != 0: self.board[i][x-1] = 1
                    if x != (self.size - 1): self.board[i][x+1] = 1
            i = y
            a = 8 if self.size == 10 else 4
            while i <= a:
                i += 1
                if self.board[i][x] != 3: # Если крестика нет, значит граница корабля, обводим
                    self.board[i][x] = 1
                    if x != 0: self.board[i][x-1] = 1
                    if x != (self.size - 1): self.board[i][x+1] = 1
                    break
                else: # если в левой клетке 3, то корабль это тело горизонтального корабля, ставим * вверху и внизу
                    if x != 0: self.board[i][x-1] = 1
                    if x != (self.size - 1): self.board[i][x+1] = 1
        return self.board

    def check_victory(self):
        a=0
        for i in self.board: a = a + (sum(x == 3 for x in i))
        if self.size == 10 and a == 20: return True
        if self.size == 6 and a == 11: return True
        return False



class Game:
    def __init__(self, size):
        self.size = size

    def new_board(self): # Получаем оба поля с расстановкой кораблей
        self.board_comp = Board(self.size)
        self.board_comp = self.board_comp.random_board
        self.board_user = Board(self.size)
        self.board_user = self.board_user.random_board

    def go(self):
        board = Out_board(self.size, self.board_user, self.board_comp)
        result = Shot_processing(self.size, self.board_comp)
        board.print_board()
        while True: # общий цикл игры
            while True: # цикл игрока
                user_shot = result.step_user()
                result_shot = result.result_shot(user_shot)
                self.board_comp = result.changing_board(result_shot)
                board.print_board()
                a = "АБВГДЕЖЗИК"
                print("Твой выстрел:", str(str(a[user_shot[1]]) + str(user_shot[0])), "(" + result_shot + ")")
                victory = result.check_victory()
                if victory:
                    print("Победа! Ты уничтожил все корабли коварного врага! Ты спас этот мир!")
                    break
                if result_shot == "мимо":
                    print("Теперь враг целится, сейчас будет выстрел!")
                    time.sleep(2)
                    break
            if victory: break
            print("стреляет комп")
            result = Shot_processing(self.size, self.board_user)
            ai_shot = None
            while True:  # цикл компа
                ai_shot = result.step_ai(ai_shot)
                result_shot = result.result_shot(ai_shot)
                self.board_user = result.changing_board(result_shot)
                board.print_board()
                a = "АБВГДЕЖЗИК"
                print("Выстрел врага:", str(str(a[ai_shot[1]]) + str(ai_shot[0])), "(" + result_shot + ")")

                time.sleep(2)
                # break

    def start(self):
        self.new_board()
        self.go()

g = Game(size)
g.start()

# 0 - пусто
# 1 - промазал
# 2 - корабль
# 3 - попал