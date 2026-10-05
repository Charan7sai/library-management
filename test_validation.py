from pymongo.errors import WriteError, DuplicateKeyError
from db import db

def attempt(label, doc, collection):
    try:
        db[collection].insert_one(doc)
        print(f"[FAIL] {label}: was accepted (it should be rejected)")
    except (WriteError, DuplicateKeyError) as e:
        print(f"[OK]   {label}: rejected")

attempt("Book missing title", {"isbn": "X1", "author": "A", "genres": [], "totalCopies": 1, "availableCopies": 1}, "books")
attempt("Negative copies", {"isbn": "X2", "title": "T", "author": "A", "genres": [], "totalCopies": -1, "availableCopies": 0}, "books")
attempt("Duplicate ISBN", {"isbn": "978-1-0000-0001-0", "title": "T", "author": "A", "genres": [], "totalCopies": 1, "availableCopies": 1}, "books")
attempt("Bad email format", {"name": "X", "email": "not-an-email", "membershipType": "student", "joinedOn": __import__("datetime").datetime.now()}, "members")