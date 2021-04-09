# В  проекте «Дом питомца» предполагается новая услуга: электронный кошелек. То есть система будет хранить данные
# о своих клиентах и их финансовых операциях. Вам нужно написать программу, обрабатывающую данные, и на выходе в
# консоль получить следующее: Клиент «Иван Петров». Баланс: 50 руб.

class Financial_transactions:
    name = None
    surname = None
    cash = None
    def __init__(self, name="unknown", surname="unknown", cash=0):
        self.name = name
        self.surname = surname
        self.cash = cash

    def set_name(self, name):
        self.name = str(name)
    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname
    def set_surname(self, surname):
        self.surname = str(surname)

    def get_cash(self):
        return self.cash
    def set_cash(self, cash):
        if cash >= 0 and isinstance(cash, int):
            self.cash = cash

    def cash_info(self):
        print("Клиент «" + self.get_name() + " " + self.get_surname() + "». Баланс: " + str(self.get_cash()) + "руб.")

client1 = Financial_transactions()
client1.set_name("Иван")
client1.set_surname("Петров")
client1.set_cash(50)

client2 = Financial_transactions()
client2.set_name("Алексей")
client2.set_surname("Ерастов")
client2.set_cash(5000)

client1.cash_info()
client2.cash_info()