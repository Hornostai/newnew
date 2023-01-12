from collections import UserDict


class Field: # батько для Name, Phone
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Name(Field): #наслідується від FIeld і має вже поле value
    pass


class Phone(Field):  #наслідується від FIeld і має вже поле value
    pass


class Record:
    def __init__(self, name, phone=None):
        self.name = name
        if phone:
            self.phones = [phone]
        else:
            self.phones = []

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phones.remove(phone)

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        self.phones.remove(phone)
        self.phones.append(new_phone)

    def __repr__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phones])}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record


"""Функції для роботи консольного бота"""


def input_error(func):
    def wrapper(*args):
        try:
            return func (*args)
        except KeyError:
            print("Give me name and phone please")
        except ValueError:
            print("Enter user name")
        except IndexError:
           print('Check your input and try again')
        except TypeError:
            print('TypeError')
    return wrapper


def add_contact(*args:str):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = Record(name,phone)
    PHONE_VOCABULAR.add_record(rec)
    # if name in PHONE_VOCABULAR.keys():
    #     user = PHONE_VOCABULAR.get(name)
    #     user['phones'].append(phone)
    # else:
    # PHONE_VOCABULAR[name] = {'name': name, 'phones': [phone]}
    print(f'Contact {name} with phone: {phone} was created!')



@input_error
def simple_func(args: str):
    return args.upper()
def greeting():
    print("How can I help you?")


@input_error
def show_all(*args):
    result = 'List of all users:'
    for key in PHONE_VOCABULAR:
        result += f'\n{PHONE_VOCABULAR[key]}'
    print(result)


def exiting():
    print('Goodbye')


def unknown(*args):
    print('Command not exist.')


@input_error
def change(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    for key in Phone.edit_phone:  
        result += key.edit_phone(args[1]),(args[2])
    print(f'Phone {old_phone} with {name}, was changed to {new_phone}')

@input_error
def show_phone(*args):
    result = "List of all phones"
    for value in Phone:
        result += f"\n{Phone[value]}"
    print(result)


COMMANDS = {
    greeting: ["hello"],
    add_contact: ['add', 'додай', "+"], #add + name + numer
    exiting: ['exit', 'close', '.'],
    change: ["change", 'edit'], # change + name + numer + new numer
    show_phone: ["phone" ], # phone + name
    show_all: ["show","all"]
}
def command_parser(user_input: str):
    for command, key_words in COMMANDS.items():
        for key_word in key_words:
            if user_input.startswith(key_word):
                return command, user_input.replace(key_word, "").split()
    return unknown, None
def main():
    while True:
        user_input = input('>>> ')
        if user_input in COMMANDS[exiting]:
            exiting()
            break
        command, data = command_parser(user_input)
        if data:
            command(*data)
        else:
            command()
if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
    print('All Ok)') #тести пройшли
    """Командний бот"""
    PHONE_VOCABULAR =  AddressBook()
    main()