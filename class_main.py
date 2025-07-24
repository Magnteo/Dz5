from class_error import input_error
from collections import UserDict
import datetime
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
        self.birthday = Birthday(birthday)

             

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
        result = []
        today = datetime.date.today()
        end_date = today +datetime.timedelta(days=days)

        for record in self.data.values():
            if record.birthday is None:
                continue
            
            bday_str = record.birthday.value
            bday = datetime.datetime.strptime(bday_str,"%d.%m.%Y").date()
            bday_this_year = bday.replace(year = today.year)
            if bday_this_year <today:
                bday_this_year = bday_this_year.replace(year=today.year +1)
            if today<= bday_this_year <=end_date:
                if bday_this_year.weekday() >=5:
                    delta_day = 7 - bday_this_year.weekday()
                    bday_this_year +=datetime.timedelta(days=delta_day)
            result.append({"name":record.name.value, "birthday":bday_this_year.strftime("%d.%m.%Y")})
        return result
    def __str__(self):
        if not self.data:
            return"No contacts"
        return'\n'.join(str(record) for record in self.data.values())        
class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")




@input_error
def add_birthday(args, book):
    name = args[0]
    birthday =args[1]
    record = book.find(name)
    if record is not None:
        record.add_birthday(birthday)
        return "update"
    return None
    
@input_error
def add_contacd(args, book: AddressBook):
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
        return record.birthday.value
    else:
        return None
@input_error
def birthdays(args, book:AddressBook):
    upcoming =  book.get_upcoming_birthdays()
    if not upcoming:
        return"No upcoming birthdays"
    result = []
    for item in upcoming:
        result.append(f"{item['name']}:{item['birthday']}") 
    return "\n".join(result)

@input_error
def all(book:AddressBook):
    if not book.data:
        return"No contacts"
    result=[]
    for record in book.values():
        result.append(str(record))
    return "\n".join(result)

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