##### README #####
# Сначала стал делать используя "алгоритм практического задания", но точно если следовать
# его правилам, то код получается практически копией кода, приложенного к вебинару "разбор проекта"
# Поэтому часть, отвечающая за расстановку кораблей идентична. После этой первой части программы,
# решил делать без помощи данных материалов
# При оценке прошу учесть что выполнены ВСЕ требования, на странице задания C2.5
#  - Для представления корабля на игровой доске есть класс Ship
#  - Есть класс доски, на которую будут размещаться корабли
#  - Корабли находятся на расстоянии минимум одна клетка друг от друга
#  - При ошибках хода игрока возникает исключение
#  - Есть исключения для непредвиденных ситуациий
#    Дополнительно:
#  - Предложено 2 варианта доски (6х6 и 10х10)
#  - Отображение информации на поле как в классической игре
#  - Для ввода координат используются не цифра + цифра, а буква + цифра (как в классике)
#  - Производится более глубокая обработка введеных пользователем координат (не обязательно
#  разделять пробелом, можно менять местами, заглавные или строчные руссие символы, итп)
#  - AI действует как человек: если ранил, то прощупывает соседние клетки чтобы добить,
#  а не рандмно палит по всей доске как в вебинаре

from random import randint
from random import choice
import time

############### НАСТРОЙКИ ИГРЫ ##############
enemy_visibility = 0 # 0 - Корабли врага скрыты, 1 - раскрыты
color = 1 # 0 - Вывод игрового поля без цвета, если наблюдается некорректное отображение, 1 - с цветом
#############################################

clear = "\n" * 2
print("\nПривет! Давай сыграем в морской бой!")
print("Есть два варианта игры - поле 6х6 и 7 кораблей, и поле 10х10 на котором 10 кораблей.")
print("Выиграет сильнейший!")
try:
    size = int(input("Выбери размер поля: 6х6 или 10х10 клеток (жми 6, если хочешь маленькое поле, иначе будет 10х10): "))
    if size != 6: size = 10
except ValueError:
    size = 10

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class BoardWrongShipException(Exception):
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
                except: pass

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
                print("        Твое поле боя:", " " * 22, "Поле боя вражеского AI:")
                if color == 1:
                    print("  \033[4mА  Б  В  Г  Д  Е  Ж  З  И  К\033[0m" + " " * 12 + "\033[4mА  Б  В  Г  Д  Е  Ж  З  И  К\033[0m")
                else:
                    print("  А  Б  В  Г  Д  Е  Ж  З  И  К" + " " * 12 + "А  Б  В  Г  Д  Е  Ж  З  И  К")
            else:
                print("   Твое поле боя:", " " * 10, "Поле боя вражеского AI:")
                if color == 1:
                    print("  \033[4mА  Б  В  Г  Д  Е\033[0m" + " " * 12 + "\033[4mА  Б  В  Г  Д  Е\033[0m")
                else: print("  А  Б  В  Г  Д  Е" + " " * 12 + "А  Б  В  Г  Д  Е")

            board_user_iter = iter(self.board_user)
            board_comp_iter = iter(self.board_comp)
            for i in range(0, self.size):
                p2 = str("  ".join(map(str, next(board_comp_iter))))
                if enemy_visibility == 0:
                    p2 = p2.replace("2", "0") # Стираем с доски корабли противника (AI)
                board = str("|" + "  ".join(map(str, next(board_user_iter))) + "|" + " " * 10 + "|" + p2 + "|")  # Собираем строку
                board = board.replace("1", "*")  # Тут и далее конвертируем цифры в отображаемые элементы
                board = board.replace("0", "·")
                board = board.replace("2", "■")
                if color == 1:
                    board = board.replace("3", "\033[31m\033[5mХ\033[0m")
                else:
                    board = board.replace("3", "Х")
                # if self.size == 10:
                #     board = board[:30] + str(i) + board[30:39] + str(i) + board[39:]
                # else:
                #     board = board[:18] + str(i) + board[18:28] + str(i) + board[28:]
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
        print("Сейчас твой ход! Введи на русском координаты (пример: А0), можно без пробела!")
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
                    print("Проверь введёные координаты! ( распознано", user_xy, ") Введи букву и цифруиз тех, что на доске!")
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

    def step_ai(self, old_ai_shot):
        self.old_ai_shot = old_ai_shot
        if old_ai_shot is not None: # Если корабль остался недобитым, щупаем в какую сторону добивать
            y = self.old_ai_shot[0]
            x = self.old_ai_shot[1]

            # print("Начало, получены координаты:", x, y)
            # Надо определить прощупать крестики как слева так и справа, потом двигаться
            # последовательно влево потом вправо до срабатывания выстрела
            h = 0
            if x != 0 and self.board[y][x - 1] == 3: h = 1
            try:
                if x != (self.size - 1) and self.board[y][x + 1] == 3: h = 1
            except IndexError: pass
            if h == 1: # корабль расположен горизонтально
                i = x
                while i >= 1: # движемся влево
                    if self.board[y][i-1] == 1: break # Если в клетке "мимо" то прерываем движ в эту сторону
                    if self.board[y][i-1] != 3: return [y, (i-1)]  # Если в клетке нет "ранен" - выстрел
                    i -= 1
                i = x # движемся вправо
                a = 9 if self.size == 10 else 5
                while i <= a:
                    if self.board[y][i+1] == 1: break # Если в клетке "мимо" то прерываем движ в эту сторону
                    if self.board[y][i+1] != 3: return [y, (i+1)]  # Если в клетке нет "ранен" или "мимо" - выстрел
                    i += 1

            v = 0
            if y != 0 and self.board[y-1][x] == 3: v = 1
            try:
                if y != (self.size - 1) and self.board[y+1][x] == 3: v = 1
            except IndexError: pass

            if v == 1: # корабль расположен вертикально
                i = y
                while i >= 1: # движемся вверх
                    if self.board[i - 1][x] == 1: break  # Если в клетке "мимо" то прерываем движ в эту сторону
                    if self.board[i - 1][x] != 3: return [(i - 1), x]  # Если в клетке нет "ранен" - выстрел
                    i -= 1
                i = y # движемся вниз
                a = 9 if self.size == 10 else 5
                while i <= a:
                    if self.board[i+1][x] == 1: break # Если в клетке "мимо" то прерываем движ в эту сторону
                    if self.board[i+1][x] != 3: return [(i + 1), x]  # Если в клетке нет "ранен" или "мимо" - выстрел
                    i += 1

            # print("Рандомный выстрел после первого попадания")
            c = 0
            while c < 10: # А если было первое попадание, то стреляем наугад в соседнюю клетку
                a = randint(0, 1) # Выбор направления выстрела (0 - горизонталь / 1 - вертикаль)
                b = choice([-1, 1]) # Выбор стороны смещения выстрела
                # print(a,b)
                c += 1
                try:
                    if a == 0:
                        if x != 0 and b != -1: # рандомный выстрел после ранения не должен перескочить на противположную сторону
                            if self.board[y][x+b] == 0 or self.board[y][x+b] == 2: return [y, (x + b)]
                    if a == 1:
                        if y != 0 and b != -1:
                            if self.board[y+b][x] == 0 or self.board[y+b][x] == 2: return [(y + b), x]
                except IndexError:
                    pass
                    # print("отловлена ошибка: IndexError: list index out of range")


        while True: # Если недобитых кораблей небыло, стреляем наугад
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

            # print("тест, вычисление корабля: ", ship)
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
        # result = Shot_processing(self.size, self.board_comp)
        old_ai_shot = None
        board.print_board()
        while True: # общий цикл игры
            result = Shot_processing(self.size, self.board_comp)
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
                    time.sleep(4)
                    break
            if victory: break
            result = Shot_processing(self.size, self.board_user)
            while True:  # цикл компа
                ai_shot = result.step_ai(old_ai_shot)
                result_shot = result.result_shot(ai_shot)
                self.board_user = result.changing_board(result_shot)
                board.print_board()
                a = "АБВГДЕЖЗИК"
                print("Выстрел врага:", str(str(a[ai_shot[1]]) + str(ai_shot[0])), "(" + result_shot + ")")
                time.sleep(2)
                victory = result.check_victory()
                if victory:
                    print("Ты потерпел поражение! Компьютер уничтожил все твои корабли, и теперь идет завоевывать весь мир!")
                    break
                if result_shot == "мимо": break
                if result_shot == "ранил": old_ai_shot = ai_shot
                if result_shot == "убил": old_ai_shot = None

            if victory: break

    def start(self):
        self.new_board()
        self.go()

g = Game(size)
g.start()

# 0 - пусто
# 1 - промазал
# 2 - корабль
# 3 - попал