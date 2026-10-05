from datetime import datetime
from pymongo.errors import DuplicateKeyError, WriteError
from db import db


# ---------- BOOKS ----------
def add_book(isbn, title, author, genres, copies, year=None):
    doc = {
        "isbn": isbn, "title": title, "author": author, "genres": genres,
        "totalCopies": copies, "availableCopies": copies,
    }
    if year:
        doc["year"] = year
    try:
        return db.books.insert_one(doc).inserted_id
    except DuplicateKeyError:
        raise ValueError("A book with this ISBN already exists")
    except WriteError:
        raise ValueError("Book failed database validation")


def get_book(isbn):
    return db.books.find_one({"isbn": isbn})


def list_books(limit=20):
    return list(db.books.find().sort("title", 1).limit(limit))


def update_book(isbn, **changes):
    book = get_book(isbn)
    if not book:
        raise ValueError("Book not found")
    if not changes:
        raise ValueError("Nothing to update")

    update = {"$set": changes}
    if "totalCopies" in changes:
        delta = changes["totalCopies"] - book["totalCopies"]
        if book["availableCopies"] + delta < 0:
            raise ValueError("Total copies cannot go below the number currently on loan")
        update["$inc"] = {"availableCopies": delta}
    try:
        db.books.update_one({"isbn": isbn}, update)
    except WriteError:
        raise ValueError("Update failed database validation")


def delete_book(isbn):
    book = get_book(isbn)
    if not book:
        raise ValueError("Book not found")
    if db.loans.count_documents({"bookId": book["_id"], "returnedOn": None}) > 0:
        raise ValueError("Cannot delete: this book has active loans")
    db.books.delete_one({"_id": book["_id"]})


# ---------- MEMBERS ----------
def add_member(name, email, phone, membership_type):
    doc = {
        "name": name, "email": email, "phone": phone,
        "membershipType": membership_type, "joinedOn": datetime.now(),
    }
    try:
        return db.members.insert_one(doc).inserted_id
    except DuplicateKeyError:
        raise ValueError("A member with this email already exists")
    except WriteError:
        raise ValueError("Member failed database validation (check email and type)")


def get_member(email):
    return db.members.find_one({"email": email})


def list_members(limit=20):
    return list(db.members.find().sort("name", 1).limit(limit))


def update_member(email, **changes):
    if not get_member(email):
        raise ValueError("Member not found")
    if not changes:
        raise ValueError("Nothing to update")
    try:
        db.members.update_one({"email": email}, {"$set": changes})
    except DuplicateKeyError:
        raise ValueError("That email is already used by another member")
    except WriteError:
        raise ValueError("Update failed database validation")


def delete_member(email):
    member = get_member(email)
    if not member:
        raise ValueError("Member not found")
    if db.loans.count_documents({"memberId": member["_id"], "returnedOn": None}) > 0:
        raise ValueError("Cannot delete: this member has unreturned books")
    db.members.delete_one({"_id": member["_id"]})