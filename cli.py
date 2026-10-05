import crud
import loans


def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def show_book(b):
    print(f"{b['isbn']} | {b['title']} by {b['author']} | "
          f"{', '.join(b['genres'])} | {b['availableCopies']}/{b['totalCopies']} available")


def show_member(m):
    print(f"{m['name']} | {m['email']} | {m['phone']} | {m['membershipType']}")


def run(action):
    try:
        action()
    except ValueError as e:
        print("Error:", e)


def add_book():
    isbn = input("ISBN: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    genres = [g.strip() for g in input("Genres (comma separated): ").split(",") if g.strip()]
    copies = ask_int("Copies: ")
    year = ask_int("Year: ")
    crud.add_book(isbn, title, author, genres, copies, year)
    print("Book added.")


def view_book():
    b = crud.get_book(input("ISBN: ").strip())
    show_book(b) if b else print("Book not found.")


def list_books():
    for b in crud.list_books():
        show_book(b)


def update_book():
    isbn = input("ISBN of book to update: ").strip()
    print("Leave a field blank to keep it unchanged.")
    changes = {}
    title = input("New title: ").strip()
    author = input("New author: ").strip()
    copies = input("New total copies: ").strip()
    if title:
        changes["title"] = title
    if author:
        changes["author"] = author
    if copies:
        changes["totalCopies"] = int(copies)
    crud.update_book(isbn, **changes)
    print("Book updated.")


def delete_book():
    crud.delete_book(input("ISBN to delete: ").strip())
    print("Book deleted.")


def add_member():
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    mtype = input("Type (student/faculty/general): ").strip()
    crud.add_member(name, email, phone, mtype)
    print("Member added.")


def view_member():
    m = crud.get_member(input("Email: ").strip())
    show_member(m) if m else print("Member not found.")


def list_members():
    for m in crud.list_members():
        show_member(m)


def update_member():
    email = input("Email of member to update: ").strip()
    print("Leave a field blank to keep it unchanged.")
    changes = {}
    name = input("New name: ").strip()
    phone = input("New phone: ").strip()
    mtype = input("New type (student/faculty/general): ").strip()
    if name:
        changes["name"] = name
    if phone:
        changes["phone"] = phone
    if mtype:
        changes["membershipType"] = mtype
    crud.update_member(email, **changes)
    print("Member updated.")


def delete_member():
    crud.delete_member(input("Email to delete: ").strip())
    print("Member deleted.")

def issue_book():
    due = loans.issue_book(input("Book ISBN: ").strip(), input("Member email: ").strip())
    print("Book issued. Due on", due.strftime("%d-%m-%Y"))


def return_book():
    fine = loans.return_book(input("Book ISBN: ").strip(), input("Member email: ").strip())
    print("Book returned.", f"Fine: ₹{fine}" if fine else "No fine.")


def member_active_loans():
    items = loans.active_loans(input("Member email: ").strip())
    if not items:
        print("No active loans.")
    for title, due in items:
        print(f"{title} | due {due.strftime('%d-%m-%Y')}")


MENU = {
    "1": ("Add book", add_book),
    "2": ("View book by ISBN", view_book),
    "3": ("List books", list_books),
    "4": ("Update book", update_book),
    "5": ("Delete book", delete_book),
    "6": ("Add member", add_member),
    "7": ("View member by email", view_member),
    "8": ("List members", list_members),
    "9": ("Update member", update_member),
    "10": ("Delete member", delete_member),
    "11": ("Issue book", issue_book),
    "12": ("Return book", return_book),
    "13": ("Member's active loans", member_active_loans),
    "0": ("Exit", None),
}

while True:
    print("\n=== Library Management ===")
    for key, (label, _) in MENU.items():
        print(f"{key}. {label}")
    choice = input("Choose: ").strip()
    if choice == "0":
        break
    if choice in MENU:
        try:
            run(MENU[choice][1])
        except ValueError:
            print("Error: invalid number entered.")
    else:
        print("Invalid choice.")