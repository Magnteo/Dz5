from collections import UserDict
import datetime
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments."
        except ValueError:
            return "Invalid value."
        except KeyError:
            return "No such contact."
    return wrapper
def parse_input(user_input):
    parts  = user_input.strip().split()
    if not parts:
        return None,[]
    return parts[0].lower() , parts[1:]
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if isinstance(value ,str) and value.strip() != "":
            super().__init__(value)
        else:
            raise ValueError

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self , phone):
            phone_find = self.find_phone(phone)
            if not phone_find:
                raise ValueError
            self.phones.remove(phone_find)

    def edit_phone(self, old_phone: str, new_phone: str):
        if  not self.find_phone(old_phone):
            raise ValueError
        self.add_phone(new_phone)
        self.remove_phone(old_phone)
    def find_phone(self, phone: str) :
        for p in self.phones:
            if p.value == phone:
                  return p
        return None
    @input_error
    def add_contact(args, book):
        name, phone, *_ = args
        record = book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message
    def add_birthday(self, birthday):
        if not isinstance(birthday,datetime.datetime):
            raise ValueError
        self.birthday = Birthday(birthday.strftime("%d.%m.%Y"))

             

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    def find(self , name :str):
        return self.data.get(name , None)
    def delete(self, name: str):
        if name  in self.data:
            del self.data[name]
        else:
            return None
    def get_upcoming_birthdays(self , days=7):
        list_name_date =[]
        today = datetime.datetime.now()
        for record in self.data.values():
            if record.birthday is None:
                continue
            name = record.name.value
            birthday = record.birthday.value
            if birthday is None:
                continue
            birthday = record.birthday.value
            month = birthday.month
            day = birthday.day
            birthday_this_year = datetime.datetime(year=today.year,month=month,day=day)
            if birthday_this_year <today:
                birthday_this_year = datetime.datetime(year=today.year + 1, month=month, day=day)
            delta = (birthday_this_year - today).days
            if 0 <=delta <=7:
                list_name_date.append({"name":name ,"birthday": birthday_this_year.strftime("%d.%m.%Y")})
        return list_name_date
                
class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.datetime.strptime(value, "%d.%m.%Y")
            self.value = parsed_date
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")




@input_error
def add_birthday(args, book):
    name = args[0]
    birthday = datetime.datetime.strptime(args[1] , "%d.%m.%Y")
    record = book.find(name)
    if record is not None:
        record.add_birthday(birthday)
        return "update"
    return None
    
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    elif record.birthday :
        date = record.birthday.value.strftime("%d.%m.%Y")
        return date
    else:
        return None
@input_error
def birthdays(args, book):
    today = datetime.datetime.today()
    end =today + datetime.timedelta(days=7)
    list_birthdays =[]
    
    for record in book.values():
        if record.birthday is not None:
            day =  record.birthday.value.day
            month =  record.birthday.value.month
            date = datetime.datetime(year=today.year , month=month , day=day )
            if today <= date <= end:
                list_birthdays.append(record.name.value)
    if list_birthdays:
        return list_birthdays
    return None
@input_error
def all(book:AddressBook):
    if not book.data:
        return"No contacts"
    result=[]
    for record in book.values():
        result.append(str(record))
    return result

@input_error
def change(args,book:AddressBook):
    name, old_phone, new_phone = args
    record:Record = book.find(name)
    if record is None:
        return "Contact not found"
    record.edit_phone(old_phone,new_phone)
    return"Update"

@input_error
def phone(args , book):
    name = args[0]
    record:Record = book.find(name)
    if record is None:
        return "Contact not found"
    return ';'.join(phone.value for phone in record.phones)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args,book))

        elif command == "change":
            print(change(args,book))

        elif command == "phone":
            print(phone(args,book))

        elif command == "all":
            print(all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args,book))

        elif command == "birthdays":
            up=book.get_upcoming_birthdays()
            if up:
                for item in up:
                    print(f"{item['name']} - {item['birthday']}")
            else:
                return None

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

            



    