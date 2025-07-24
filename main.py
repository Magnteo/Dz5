from class_main import *

def parse_input(user_input):
    parts  = user_input.strip().split()
    if not parts:
        return None,[]
    return parts[0].lower() , parts[1:]


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
            print(add_contacd(args,book))

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
                print("No upcoming birthdays")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

            



    