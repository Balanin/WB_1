from collections import UserDict
from datetime import datetime
import pickle
from abc import abstractmethod, ABCMeta

def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'
    return inner

class MyBaseClass(metaclass=ABCMeta):
    @abstractmethod
    def value(self):
        pass

   

class Field(MyBaseClass):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if len(value) != 13 or value[0] != '+' or not value[1:].isdigit():
            raise ValueError('Invalid phone number.')
        self._value = value

    pass


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        if value.find('-'):
            value = value.replace("-", ".")
        list = value.split('.')
        value1 = datetime(year=int(list[-1]), month=int(list[-2]), day=int(list[0])).date()
        if value1 > datetime.now().date():
            raise ValueError("Birthday must be less than current year and date.")
        self._value = value


class Record:
    def __init__(self, name: Name, phones=None):
        self.name = Name(name)
        if phones is None:
            self.numbers = []
        else:
            self.numbers = [Phone(phones)]
        self.birthday = None

    def add_phone(self, number):
        if number not in [i.value for i in self.numbers]:
            self.numbers.append(Phone(number))

    def del_phone(self, number):
        for num in self.numbers:
            if num.value == number:
                self.numbers.remove(num)

    def add_birthday(self, day):
        self.birthday = Birthday(day)

    def change_phones(self, number):
        for i in self.numbers:
            if i.value == number[0]:
                self.numbers.remove(i)
            self.add_phone(number[1])

    def get_info(self):
        phones_info = ''
        for phone in self.numbers:
            phones_info += f'{phone.value} '
        return f'{self.name.value} : {phones_info}'

    def days_to_birthday(self):
        self.birthday
        if self.birthday.value.find('-'):
            self.birthday = self.birthday.value.replace("-", ".")

        list = self.birthday.split('.')
        this_year = datetime.now().year
        birthday = datetime(year=int(this_year), month=int(list[-2]), day=int(list[0])).date()
        current_datetime = datetime.now().date()

        if birthday < current_datetime:
            birthday = datetime(year=int(this_year) + 1, month=int(list[-2]), day=int(list[0])).date()
        return f'{birthday - current_datetime}'

    def __repr__(self):
        return f'{self.name} {self.numbers}'


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def get_record(self, name) -> Record:
        return self.data.get(name)

    def __repr__(self) -> str:
        return f'{self.data.keys}'

    def remove_record(self, name):
        del self.data[name]

    def iterator(self, count=2):
        page = []
        i = 0
        for record in self.data.values():
            page.append(record)
            i += 1
            if i == count:
                yield page
                page = []
                i = 0
        if page:
            yield page

    def search(self, value):
        record_result = []
        for record in self.get_all_record().values():
            if value in record.name.value:
                record_result.append(record)
                continue

            for phone in record.numbers:
                if value in phone.value:
                    record_result.append(record)

        if not record_result:
            raise ValueError("Contacts with this value does not exist.")
        return record_result

    def save_contacts(self):
        with open('aaaaa.pickle', 'wb') as f:
            pickle.dump(self.data, f)

    def load_contacts(self):
        with open('aaaaa.pickle', 'rb') as f:
            self.data = pickle.load(f)
            return self.data