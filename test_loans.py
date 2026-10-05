from datetime import datetime, timedelta
from db import db, SUPPORTS_TRANSACTIONS
import loans

print("Transactions supported:", SUPPORTS_TRANSACTIONS)

ISBN = "978-1-0000-0012-0"      # NoSQL Distilled, 2 copies
EMAIL = "aarav@example.com"
db.loans.delete_many({})
db.books.update_one({"isbn": ISBN}, {"$set": {"availableCopies": 2}})

def available():
    return db.books.find_one({"isbn": ISBN})["availableCopies"]

loans.issue_book(ISBN, EMAIL)
print("After issue, available =", available(), "(expected 1)")

try:
    loans.issue_book(ISBN, EMAIL)
except ValueError as e:
    print("[OK] Duplicate issue rejected:", e)

# Make the loan 5 days overdue
db.loans.update_one({"returnedOn": None}, {"$set": {"dueDate": datetime.now() - timedelta(days=5)}})

fine = loans.return_book(ISBN, EMAIL)
print("Fine =", fine, "(expected 10)")
print("After return, available =", available(), "(expected 2)")

try:
    loans.return_book(ISBN, EMAIL)
except ValueError as e:
    print("[OK] Double return rejected:", e)

# Exhaust copies
loans.issue_book(ISBN, "aarav@example.com")
loans.issue_book(ISBN, "diya@example.com")
try:
    loans.issue_book(ISBN, "rohan@example.com")
except ValueError as e:
    print("[OK] Zero copies rejected:", e)