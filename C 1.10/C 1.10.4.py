# Команда проекта «Дом питомца» планирует большой корпоратив для своих волонтеров. Вам необходимо написать
# программу, которая позволяла бы составлять список нескольких гостей. Решите задачу с помощью метода конструктора
# и примените один из принципов наследования.
# При выводе в консоль вы должны получить:  «Иван Петров, г. Москва, статус "Наставник"»


class Volunteer:
    def __init__(self, name, surname, city, status):
        self.name = name
        self.surname = surname
        self.city = city
        self.status = status

# Наследование
class Volunteer_status(Volunteer):
    def guest_info(self):
        print("«" + self.name + " " + self.surname + ", г. " + self.city + ', статус "' + self.status + '"»')

volunteers = [
    {
     "name": "Иван",
     "surname": "Петров",
     "city": "Москва",
     "status": "Наставник",
    },
    {
     "name": "Василий",
     "surname": "Сидоров",
     "city": "Одинцово",
     "status": "Наставник",
    },
    {
     "name": "Алексей",
     "surname": "Ерастов",
     "city": "Апрелевка",
     "status": "Наставник",
    },
]

# Конструктор
for record in volunteers:
    record_obj = Volunteer_status(name=record.get("name"),
                                  surname=record.get("surname"),
                                  city=record.get("city"),
                                  status=record.get("status"))
    record_obj.guest_info()


