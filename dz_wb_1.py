from Class import *

USERS = AddressBook()


# +
@ error_handler
def add_user(data):
    name, *phones = data
    if not phones or not name:
        raise TypeError
    if name in USERS:
        return ('\nThis contact already exist.\n')
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)
    USERS.add_record(record)

    return f'\nUser {name} added with number: {phone}\n'


# +
@ error_handler
def delete_contact(data):
    name, *args = (data)
    if  not name:
        raise TypeError
    if name not in USERS.data.keys():
        return f'\nContact with name {name} not found!\n'
    else:
        USERS.remove_record(name)
        return f'\nContact {name} has been deleted \n'



@ error_handler
def delete_phone(data):
    name, *phone = (data)
    if not phone or not name:
        raise TypeError
    if name not in USERS:
        return f'\nContact with name {name} not found! \n'
    else:
        contact = USERS[name]
        contact.del_phone(*phone)
        return f'\nNumber {phone[0]} has been deleted from {name}\n'


@ error_handler
def addd_phone(data):
    name, *phones = data
    if not phones or not name:
        raise TypeError
    if name in USERS:
        record = USERS[name]
        for phone in phones:
            record.add_phone(phone)
        return f'\nUser {name} changed the get new number: \n'



@ error_handler
def change_phone(data):
    name, *phone = data
    if not phone or not name:
        raise TypeError
    record = USERS[name]
    record.change_phones(phone)
    return f'\nUser {name} changed the phone, his new number: {phone[1]}\n'



@ error_handler
def show_all(contacts, *args):
    if not contacts:
        return 'Address book is empty'
    result = 'List of all users:\n'
    phone_book = USERS.iterator()
    for contact in phone_book:  
        for i in contact:
            result +=  f'{i.name.value}:'
            for number in i.numbers:
                result += f' {number.value} ' 
            result += '\n'
    return  '\n' + result 
    

@ error_handler
def show_phone(data):
    name = data[0]
    if  not name:
        raise TypeError
    record = USERS[name]
    return f'\n{record.get_info()}\n'

@ error_handler
def birthday(data):
    name, day = data
    if not day or not name:
        raise TypeError
    record = USERS[name]
    record.add_birthday(day)
    return f'\nBirthday added on {day}\n'

@ error_handler
def next_birthday(data):
    name, *args = data
    if not name:
        raise TypeError
    record = USERS[name]
    x = record.days_to_birthday()
    return f'\nUntil the next birthday {x}\n'


def hello(_):
    return "\nHow can I help you?\n"


def exit(_):
    print("\nGood bye!\n")
    USERS.save_contacts()
    sys.exit()


def load_book(_):
    USERS.load_contacts()
    return '\nBook is loaded\n'


def search(data):
    data = ''.join(data)
    search_records = ''
    records = USERS.search(data)

    for record in records:
        search_records += f'{record.get_info()}\n'
    return f'\nSearch results:\n{search_records}\n'


HANDLER = {

    "hello": hello,
    "good bye": exit,
    "close": exit,
    "exit": exit,
    "add contact": add_user,
    "add phone": addd_phone,
    "delete": delete_contact,
    "del phone": delete_phone,
    "show all": show_all,
    "change": change_phone,
    "phone": show_phone,
    "add birthday": birthday,
    "next birthday": next_birthday,
    "load": load_book,
    "search user": search

}


def parser(user_input):
    new_input = user_input
    data = ''
    for key in HANDLER:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            data = data.strip().split(' ')

            break
    if data:
        return reaction_func(new_input)(data)


def reaction_func(reaction):
    return HANDLER.get(reaction, break_func)


def break_func():
    return '\nWrong enter.\n'


def main():
    while True:
        user_input = input('>>> ')
        result = parser(user_input)
        print(result)


if __name__ == "__main__":
    main()
