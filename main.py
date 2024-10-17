from collections import UserDict
from datetime import datetime, timedelta
import regex
from colorama import Fore
import pickle


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        self.value = value
        super().__init__(value)


class Phone(Field):

    def __init__(self, value: str):
        try:
            value = self.__use_check_Phone(value)
        except ValueError:
            raise ValueError(f"this phone {value} is not correct")
        super().__init__(value)

    def __use_check_Phone(self, phone: str):
        pettern_1 = r"\D"
        matches = regex.sub(pettern_1, "", phone)
        check_number = bool(regex.search(r"^380\d{9}$", matches))
        check_num = bool(regex.search(r"^0\d{9}$", matches))
        check_n = bool(regex.search(r"^+380\d{9}$", matches))
        if check_number:
            number = "+" + matches
            dict_name_phone = number
            return dict_name_phone
        elif check_num:
            number_1 = "+38" + matches
            dict_name_phone_1 = number_1
            return dict_name_phone_1
        elif check_n:
            dict_name_phone2 = matches
            return dict_name_phone2
        else:
            raise ValueError

    def __str__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = self.__check_ditetime(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __check_ditetime(self, value: str):
        datetime_object = datetime.strptime(value, "%d.%m.%Y")
        return datetime_object

    # def __str__(self):
    #     return f"birthday {self.value.date()}"

    def __str__(self):
        return self.value.date().__str__()


class Record:

    def __init__(self, name: str):
        self.name = Name(name)
        self.phone = []
        self.birthday = None

    def __getstate__(self):
        state = self.__dict__
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def add_Phone(self, phone: str):
        if phone not in self.phone:
            new_phone_user = Phone(phone)
            return self.phone.append(new_phone_user.value)
        else:
            print("your Phone is in address book")

    def edit_Phone(self, oldPhone: str, newPhone: str):
        index = self.phone.index(oldPhone)
        result = self.phone[index] = newPhone
        return f"your new phone : {result}",

    def delete_Phone(self, phone: str):
        self.phone.remove(phone)

    def add_birthday(self, birthday_user: str):
        birthday = Birthday(birthday_user)
        self.birthday = birthday
        return birthday.value

    def show_birthday(self):
        return f"your birthday: {self.birthday}"

    def __str__(self):
        return f"name: {self.name}, phone: {self.phone}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def __dict__(self):
        for k in self.data:
            values = self.find_Phone_by_Name(k)
            return {"name": values.name.value, "phone": values.phone, "birthday": str(values.birthday)}

    def __getstate__(self):
        return self.data

    def __setstate__(self, state):
        self.update(state)

    def save_data(self, filename="address_book.txt"):
        with open(filename, "wb") as f:
           result = pickle.dump(self.__dict__(), f)
           return result

    def load_data(self, filename="address_book.txt"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()

    def add_Phone_in_book(self, record: Record):

        res = self.data[record.name.value] = record

        return res

    def find_Phone_by_Name(self, name: str) -> Record | None:
        res = self.get(name)
        if res is not None:
            return res

        else:
            return None

    def delete_Phone_by_Name(self, del_by_name: str):
        if del_by_name in self:
            self.pop(del_by_name)

    def all_name_and_phone(self):
        for k in self.data.keys():
            res = self.find_Phone_by_Name(k)
        print(f"{res.name} {res.phone} {res.birthday}")

    def __check_on_happy_birthday(self, happy_birthday: str):
        split_date = str(happy_birthday)

        result = split_date.split("-")
        my_birthday = datetime.strptime(f"{result[2]}.{result[1]}.{result[0]}", "%d.%m.%Y")
        present = datetime(day=my_birthday.day, month=my_birthday.month, year=my_birthday.now().year).date()
        if present > datetime.now().date():
            if present.isoweekday() == 1 and my_birthday.month == datetime.now().month:
                date_happy_birthday = present + timedelta(days=1)
                return date_happy_birthday.__str__()
            if present.isoweekday() == 7 and my_birthday.month == datetime.now().month:
                date_happy_birthday = present + timedelta(days=2)
                return date_happy_birthday.__str__()
            else:
                pass
        else:
            pass

    def birthdays(self):
        lists_birthday_in_week = []
        for k in self.data.keys():
            name_contact_users = self.find_Phone_by_Name(k)
            user_happy_birthday = self.__check_on_happy_birthday(name_contact_users.birthday)
            if user_happy_birthday is not None:
                lists_birthday_in_week.append(f"{k} : {user_happy_birthday}")
                return lists_birthday_in_week


book = AddressBook()
print(F"{Fore.LIGHTBLUE_EX}Hello my Friend")
print("I am assistant bot!")
while True:
    book.load_data()
    print("select a command", "--->__add_Name_and_Phone<---> add")
    print("select a command", "--->__change_Phone<---> change")
    print("select a command", "--->__show_Name_by_Phone<---> show")
    print("select a command", "--->__all_Name_and_Phone<---> all")
    print("select a command", "--->__del_Name_and_Phone<---> del")
    print("select a command", "--->__add_birthday<---> add_birthday")
    print("select a command", "--->show_birthday_user<---> show_birthday")
    print("select a command", "--->birthdays_all_users<---> birthdays")
    command = input().__str__().lower().strip()
    if command == "add":
        print(F"{Fore.LIGHTYELLOW_EX}Your name and number Phone")
        name = input(F"{Fore.LIGHTYELLOW_EX}please your name:").strip().lower()
        phone = input(F"{Fore.LIGHTYELLOW_EX}please your phone :").strip().lower()
        record = Record(name)
        check_Phone1 = Phone(phone)
        record.add_Phone(check_Phone1.value)
        book.add_Phone_in_book(record)
        print(f"{record.name}, {record.phone}")
    if command == "change":
        print("Please your name and the new phone and old phone you want to replace")
        name_user = input("your name :").strip().lower()
        phone_Old = input("your old phone :").strip().lower()
        phone_New = input("you new phone :").strip().lower()

        name_this_address = book.find_Phone_by_Name(name_user)

        ch_ph_old = Phone(phone_Old)
        ch_ph_new = Phone(phone_New)

        result = name_this_address.edit_Phone(str(ch_ph_old), str(ch_ph_new))
        print(result)
    if command == "show":
        namePhoneFind = input("your name: ").strip().lower()
        show_phone_by_name = book.find_Phone_by_Name(namePhoneFind)
        if show_phone_by_name is not None:
            print(show_phone_by_name)
        else:
            print("your number phone is not address book")
    if command == "all":
        book.all_name_and_phone()
    if command == "del":
        name = input(F"{Fore.LIGHTYELLOW_EX}please your name: ").strip().lower()
        book.delete_Phone_by_Name(name)
    if command == "add_birthday":
        name = input("your name: ").strip().lower()
        your_birthday = input("your birthday ? and please use format DD.MM.YYYY: ")
        name_set_birthday = book.find_Phone_by_Name(name)
        name_set_birthday.add_birthday(your_birthday)
        print(f"your birthday add address_book: {name_set_birthday.birthday}")
    if command == "show_birthday":
        name = input("please your name: ")
        name_contact = book.find_Phone_by_Name(name)
        print(name_contact.birthday)
    if command == "birthdays":
        birthdays_in_week = book.birthdays()
        print(f"all birthday in week: {birthdays_in_week}")
    if command in ["close", "exit"]:
        book.save_data()
        print("Good bye my Friend!")
        break