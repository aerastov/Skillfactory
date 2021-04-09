class Cat:
    name = None
    gender = None
    age = None
    def __init__(self, name="unknown", gender="unknown", age="unknown"):
        self.name = name
        self.gender = gender
        self.age = age

    def set_name(self, name):
        self.name = str(name)

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender
    def set_gender(self, gender):
        if gender == "мальчик" or gender == "девочка":
            self.gender = gender

    def get_age(self):
        return self.age
    def set_age(self, age):
        if age > 0 and isinstance(age, int):
            self.age = age

    def cat_info(self):
        print("\nИмя: " + self.get_name() + "\nПол: " + self.get_gender() + "\nВозраст: " + str(self.get_age()))