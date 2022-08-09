a, b, c = str("---"), str("---"), str("---")
clear = "\n" * 10
user_symbol = "x"
python_symbol = "o"
comp_victory = ["Чтобы закончить игру, нужно меня победить!", "Человек не может быть умнее компьютера, я победил тебя",
                "Ты у меня все равно не выиграешь! Никогда!", "Придется играть еще и еще, чтобы у меня выиграть!",
                "Так мы будем играть всю твою жизнь... Попробуй обыграть уже...", "Не хочу хвастаться, но человеку до меня далеко! Даже не мечтай!",
                "Сегодня проиграл машине в крестики нолики, завтра ИИ захватит мир!"]
import random

def print_abc(a, b, c):
    print("   0 1 2")
    print("0 ", a[0], a[1], a[2])
    print("1 ", b[0], b[1], b[2])
    print("2 ", c[0], c[1], c[2])

def input_user():
    return input("Твой ход! (ты крестик, одной строкой вводи координаты по горизонтали и вертикали: ")

def check_user_xy(user_xy): # Проверка и очистка того, что ввел юзер
    for i in range(len(user_xy)):  # Проверим, что там ввел юзер и уберем лишнее
        if user_xy[i] not in "012":
            user_xy = user_xy.replace(user_xy[i], " ")
    user_xy = user_xy.replace(" ", "") # Теперь удалим пробелы, (в цикле нельзя - меняется длинна строки - ошибка)
    return user_xy

def who_is_winner(a,b,c): # Проверка, есть ли победитель?
    if a[0] == a[1] == a[2] == user_symbol or b[0] == b[1] == b[2] == user_symbol or c[0] == c[1] == c[2] == user_symbol: return "user"
    if a[0] == b[1] == c[2] == user_symbol or a[2] == b[1] == c[0] == user_symbol: return "user"
    if a[0] == b[0] == c[0] == user_symbol or a[1] == b[1] == c[1] == user_symbol or a[2] == b[2] == c[2] == user_symbol: return "user"
    if a[0] == a[1] == a[2] == python_symbol or b[0] == b[1] == b[2] == python_symbol or c[0] == c[1] == c[2] == python_symbol: return "python"
    if a[0] == b[1] == c[2] == python_symbol or a[2] == b[1] == c[0] == python_symbol: return "python"
    if a[0] == b[0] == c[0] == python_symbol or a[1] == b[1] == c[1] == python_symbol or a[2] == b[2] == c[2] == python_symbol: return "python"
    if len(a.replace("-", "")) == 3 and len(b.replace("-", "")) == 3 and len(c.replace("-", "")) == 3: return "draw"
    return None



#### Ох тут жара щас будет, комп решает как сходить)) ####

def f_step_python(a,b,c):
    ### Ход в центр, если не занят
    if b[1] == "-": return [a, str(b[:1] + python_symbol + b[2:]), c]

    ### Далее ход в третью клетку и победа, если комп уже выстроил в линию 2 клетки
    if len(a.replace(python_symbol, "")) == 1 and "-" in a: return [a.replace("-", python_symbol), b, c] # По горизонтали a
    if len(b.replace(python_symbol, "")) == 1 and "-" in b: return [a, b.replace("-", python_symbol), c] # По горизонтали b
    if len(c.replace(python_symbol, "")) == 1 and "-" in c: return [a, b, c.replace("-", python_symbol)] # По горизонтали c

    d = str(a[0] + b[0] + c[0]) # Выигрыш по вертикали первый ряд
    if len(d.replace(python_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(python_symbol + a[1:])
        if d.find('-') == 1: b = str(python_symbol + b[1:])
        if d.find('-') == 2: c = str(python_symbol + c[1:])
        return [a, b, c]

    d = str(a[1] + b[1] + c[1]) # Выигрыш по вертикали второй ряд
    if len(d.replace(python_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(a[0] + python_symbol + a[2])
        if d.find('-') == 1: b = str(b[0] + python_symbol + b[2])
        if d.find('-') == 2: c = str(c[0] + python_symbol + c[2])
        return [a, b, c]

    d = str(a[2] + b[2] + c[2]) # Выигрыш по вертикали третий ряд
    if len(d.replace(python_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(a[:2] + python_symbol)
        if d.find('-') == 1: b = str(b[:2] + python_symbol)
        if d.find('-') == 2: c = str(c[:2] + python_symbol)
        return [a, b, c]

    d = str(a[0] + b[1] + c[2]) # Выигрыш по диагонали 1
    if len(d.replace(python_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(python_symbol + a[1:])
        if d.find('-') == 1: b = str(b[0] + python_symbol + b[2])
        if d.find('-') == 2: c = str(c[:2] + python_symbol)
        return [a, b, c]

    d = str(a[2] + b[1] + c[0]) # Выигрыш по диагонали 2
    if len(d.replace(python_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(a[:2] + python_symbol)
        if d.find('-') == 1: b = str(b[0] + python_symbol + b[2])
        if d.find('-') == 2: c = str(python_symbol + c[1:])
        return [a, b, c]

    ### Далее ходы в третью клетку, если юзер уже выстроил в линию 2 клетки

    if len(a.replace(user_symbol, "")) == 1 and "-" in a: return [a.replace("-", python_symbol), b, c] # По горизонтали a
    if len(b.replace(user_symbol, "")) == 1 and "-" in b: return [a, b.replace("-", python_symbol), c] # По горизонтали b
    if len(c.replace(user_symbol, "")) == 1 and "-" in c: return [a, b, c.replace("-", python_symbol)] # По горизонтали c

    d = str(a[0] + b[0] + c[0]) # По вертикали первый ряд
    if len(d.replace(user_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(python_symbol + a[1:])
        if d.find('-') == 1: b = str(python_symbol + b[1:])
        if d.find('-') == 2: c = str(python_symbol + c[1:])
        return [a, b, c]

    d = str(a[1] + b[1] + c[1]) # По вертикали второй ряд
    if len(d.replace(user_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(a[0] + python_symbol + a[2])
        if d.find('-') == 1: b = str(b[0] + python_symbol + b[2])
        if d.find('-') == 2: c = str(c[0] + python_symbol + c[2])
        return [a, b, c]

    d = str(a[2] + b[2] + c[2]) # По вертикали третий ряд
    if len(d.replace(user_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(a[:2] + python_symbol)
        if d.find('-') == 1: b = str(b[:2] + python_symbol)
        if d.find('-') == 2: c = str(c[:2] + python_symbol)
        return [a, b, c]

    d = str(a[0] + b[1] + c[2]) # По диагонали 1
    if len(d.replace(user_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(python_symbol + a[1:])
        if d.find('-') == 1: b = str(b[0] + python_symbol + b[2])
        if d.find('-') == 2: c = str(c[:2] + python_symbol)
        return [a, b, c]

    d = str(a[2] + b[1] + c[0]) # По диагонали 2
    if len(d.replace(user_symbol, "")) == 1 and "-" in d:
        if d.find('-') == 0: a = str(a[:2] + python_symbol)
        if d.find('-') == 1: b = str(b[0] + python_symbol + b[2])
        if d.find('-') == 2: c = str(python_symbol + c[1:])
        return [a, b, c]

    if a[0] == user_symbol and c[2] == "-": return [a, b, str(c[:2] + python_symbol)]
    if a[2] == user_symbol and c[0] == "-": return [a, b, str(python_symbol + c[1:])]
    if c[0] == user_symbol and a[2] == "-": return [str(a[:2] + python_symbol), b, c]
    if c[2] == user_symbol and a[0] == "-": return [str(python_symbol + a[1:]), b, c]

    # Делаем ход в случайный угол, если все остальные условия не сработали и есть свободный угол
    d = str(a[0] + a[2] + c[0] + c[2])
    while len(d.replace("-", "")) < 4:
        d1 = random.randint(0, 3)
        if d1 == 0 and c[2] == "-": return [a, b, str(c[:2] + python_symbol)]
        if d1 == 1 and c[0] == "-": return [a, b, str(python_symbol + c[1:])]
        if d1 == 2 and a[2] == "-": return [str(a[:2] + python_symbol), b, c]
        if d1 == 3 and a[0] == "-": return [str(python_symbol + a[1:]), b, c]

    # Делаем ход в оставшуюся случайную свободную клетку
    while True:
        d1 = random.randint(0, 2)
        if d1 == 0 and len(a.replace("-", "")) < 3: return [a.replace("-", python_symbol, 1), b, c]
        if d1 == 1 and len(b.replace("-", "")) < 3: return [a, b.replace("-", python_symbol, 1), c]
        if d1 == 2 and len(c.replace("-", "")) < 3: return [a, b, c.replace("-", python_symbol, 1)]


print(clear, "Давай поиграем в крестики - нолики!")
print_abc(a, b, c)
print("Даю фору, предлагаю играть крестиком! Сделай ход первым!")
while True:  # цикл начала новой игры
    while True: # цикл хода игры, пока кто-то не выиграет
        user_xy = input_user()
        while True: # Высасываем мозг до тех пор, пока не получим от юзера 2 правильные координаты
            user_xy = check_user_xy(user_xy) # Отправляем на проверку и очистку
            print(clear, "Вы не ввели координаты хода! Мне нужно знать какой Ваш ход!!!") if len(user_xy) == 0 else None
            print(clear, "Вы ввели больше 2-х значений! Соберитесь уже!") if len(user_xy) > 2 else None
            print(clear, "Вы ввели всего одну координату хода, давайте еще раз, но теперь обе!!!") if len(user_xy) == 1 else None
            if len(user_xy) == 2:
                if a[int(user_xy[1])] != "-" and user_xy[0] == "0" or b[int(user_xy[1])] != "-" and user_xy[0] == "1" or c[int(user_xy[1])] != "-" and user_xy[0] == "2":
                    print(clear, "В этой клетке уже записан ход, будь внимательнее!!!")
                    user_xy = ""
            if len(user_xy) == 2:  # условие для завершения цикла
                break
            print_abc(a, b, c)
            user_xy = input_user()


        ####  Запись в импровизированную матрицу хода игрока ####
        a = str(a[:int(user_xy[1])] + user_symbol + a[int(user_xy[1]) + 1:]) if user_xy[0] == "0" else a
        b = str(b[:int(user_xy[1])] + user_symbol + b[int(user_xy[1]) + 1:]) if user_xy[0] == "1" else b
        c = str(c[:int(user_xy[1])] + user_symbol + c[int(user_xy[1]) + 1:]) if user_xy[0] == "2" else c

        winner = who_is_winner(a,b,c) #### Проверка есть ли победитель
        if winner is not None:
            break

        step_python = f_step_python(a, b, c) # Ход компьютера
        a, b, c = str(step_python[0]), str(step_python[1]), str(step_python[2]) # Возвращаем результат функции в строки abc

        winner = who_is_winner(a,b,c) #### Проверка есть ли победитель
        if winner is not None:
            break

        print(clear, "Супер! Я тоже сделал ход! Теперь снова Твоя очередь!")
        print_abc(a, b, c)

    print(clear)

    if winner == "draw":
        print("Ничья! Ты вниматеьно играл! Можешь закончить игру, если хочешь!")
        print_abc(a, b, c)
        go = input("Хочешь закончить игру? Если да, то жми Y: ")
        if go == "Y" or go == "y" or go == "Н" or go == "н":
            break
        print(clear, "Молоток, что не сдался, но ты все равно никогда не выиграешь! Начнем снова!")
        a, b, c = str("---"), str("---"), str("---")
        print_abc(a, b, c)

    if winner == "python":
        print("Я ВЫИГРАЛ !!!")
        print(random.choice(comp_victory))
        print_abc(a, b, c)
        go = "*"
        while go != "":
            go = input("Чтобы завершить программу, придется выиграть (или хотя бы сыграть в ничью, ведь ты все равно у меня не выиграешь!) Нажми ENTER: ")
        print(clear)
        a, b, c = str("---"), str("---"), str("---")
        print_abc(a, b, c)

    if winner == "user":
        print("ТЫ ВЫИГРАЛ !!!")
        print_abc(a, b, c)
        go = input("Хочешь еще раз? Если да, то жми Y: ")
        if go == "Y" or go == "y" or go == "Н" or go == "н":
            print(clear, "Начнем снова!")
            a, b, c = str("---"), str("---"), str("---")
            print_abc(a, b, c)
        else:
            break

print("Спасибо за игру!!! Пока!")
