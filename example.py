from collections import UserDict


class Field:  # батько для Name, Phone
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Name(Field):  # наслідується від FIeld і має вже поле value
    pass

class Phone(Field):  # наслідується від FIeld і має вже поле value
    pass

class Record:
    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f"Phone for contact {self.name.value} change successful"
        return f"Contact {self.name.value} dont have phone {old_phone.value}"

    def __repr__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phones])}'
    
  
class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record


"""Функції для роботи консольного бота"""


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            print("Give me name and phone please")
        except ValueError:
            print("Enter user name")
        except IndexError:
            print("Check your input and try again")
        except TypeError:
            print("TypeError")

    return wrapper


def add_contact(*args: str):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = Record(name, phone)
    PHONE_VOCABULAR.add_record(rec)
    return f"Contact {name} with phone: {phone} was created!"


@input_error
def simple_func(args: str):
    return args.upper()


def greeting():
    return "How can I help you?"


@input_error
def show_all(*args):
    if PHONE_VOCABULAR:
        result = "List of all users:"
        for key in PHONE_VOCABULAR:
            result += f"\n{PHONE_VOCABULAR[key]}"
        return result
    return f"Phone Vocabulary dont have contact now"


def exiting():
    print ("Goodbye")


def unknown(*args):
    print ("Command not exist")


@input_error
def change(*args):
    rec = PHONE_VOCABULAR.get(args[0])
    if rec:
        old_phone = Phone(args[1])
        new_phone = Phone(args[2])
        return rec.edit_phone(old_phone, new_phone)
    return f"Contact with name {args[0]} not in AddressBook"


@input_error
def show_phone(*args):
    rec = PHONE_VOCABULAR.get(args[0])
    if rec:
        return rec
    return f"Contact with name {args[0]} is not in the phone book"


COMMANDS = {
    greeting: ["hello"],
    add_contact: ["add", "додай", "+"],  # add + name + numer
    exiting: ["exit", "close", "."],
    change: ["change", "edit"],  # change + name + numer + new numer
    show_phone: ["phone"],  # phone + name
    show_all: ["show", "all"],
}


def command_parser(user_input: str):
    for command, key_words in COMMANDS.items():
        for key_word in key_words:
            if user_input.startswith(key_word):
                return command, user_input.replace(key_word, "").split()
    return unknown, None


def main():
    while True:
        user_input = input(">>> ")
        if user_input in COMMANDS[exiting]:
            exiting()
            break
        command, data = command_parser(user_input)
        if data:
            print(command(*data))
        else:
            print(command())


if __name__ == "__main__":
    p1 = Phone('12345')
    p2 = Phone('12345')
    print(p1.value == p2.value)
    name = Name("Bill")
    phone = Phone("1234567890")
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)
    assert isinstance(ab["Bill"], Record)
    assert isinstance(ab["Bill"].name, Name)
    assert isinstance(ab["Bill"].phones, list)
    assert isinstance(ab["Bill"].phones[0], Phone)
    assert ab["Bill"].phones[0].value == "1234567890"
    print("All Ok)")  # тести пройшли
    """Командний бот"""
    PHONE_VOCABULAR = AddressBook()
    main()
