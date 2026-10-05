from datetime import datetime, timedelta
from db import db, client, SUPPORTS_TRANSACTIONS

LOAN_DAYS = 14
FINE_PER_DAY = 2
MAX_ACTIVE_LOANS = 3


def _run(fn):
    """Run fn inside a transaction if supported, otherwise run it directly."""
    if SUPPORTS_TRANSACTIONS:
        with client.start_session() as session:
            return session.with_transaction(lambda s: fn(s))
    return fn(None)


def issue_book(isbn, email):
    def work(session):
        book = db.books.find_one({"isbn": isbn}, session=session)
        member = db.members.find_one({"email": email}, session=session)
        if not book:
            raise ValueError("Book not found")
        if not member:
            raise ValueError("Member not found")

        active = db.loans.count_documents(
            {"memberId": member["_id"], "returnedOn": None}, session=session)
        if active >= MAX_ACTIVE_LOANS:
            raise ValueError(f"Member already has {MAX_ACTIVE_LOANS} active loans")

        if db.loans.find_one({"memberId": member["_id"], "bookId": book["_id"],
                              "returnedOn": None}, session=session):
            raise ValueError("Member already has this book")

        # Atomic check-and-decrement: only succeeds if a copy is available
        updated = db.books.find_one_and_update(
            {"_id": book["_id"], "availableCopies": {"$gt": 0}},
            {"$inc": {"availableCopies": -1}},
            session=session,
        )
        if not updated:
            raise ValueError("No copies available")

        now = datetime.now()
        loan = {
            "bookId": book["_id"], "memberId": member["_id"],
            "issuedOn": now, "dueDate": now + timedelta(days=LOAN_DAYS),
            "returnedOn": None, "fine": 0,
        }
        try:
            db.loans.insert_one(loan, session=session)
        except Exception:
            if session is None:  # no transaction, so undo the decrement manually
                db.books.update_one({"_id": book["_id"]}, {"$inc": {"availableCopies": 1}})
            raise
        return loan["dueDate"]

    return _run(work)


def return_book(isbn, email):
    def work(session):
        book = db.books.find_one({"isbn": isbn}, session=session)
        member = db.members.find_one({"email": email}, session=session)
        if not book or not member:
            raise ValueError("Book or member not found")

        now = datetime.now()
        loan = db.loans.find_one(
            {"bookId": book["_id"], "memberId": member["_id"], "returnedOn": None},
            session=session)
        if not loan:
            raise ValueError("No active loan found for this book and member")

        days_late = max(0, (now.date() - loan["dueDate"].date()).days)
        fine = days_late * FINE_PER_DAY

        # Filter on returnedOn: None so a double return can't happen
        result = db.loans.update_one(
            {"_id": loan["_id"], "returnedOn": None},
            {"$set": {"returnedOn": now, "fine": fine}}, session=session)
        if result.modified_count == 0:
            raise ValueError("Loan was already returned")

        db.books.update_one({"_id": book["_id"]},
                            {"$inc": {"availableCopies": 1}}, session=session)
        return fine

    return _run(work)


def active_loans(email):
    member = db.members.find_one({"email": email})
    if not member:
        raise ValueError("Member not found")
    results = []
    for loan in db.loans.find({"memberId": member["_id"], "returnedOn": None}):
        book = db.books.find_one({"_id": loan["bookId"]})
        results.append((book["title"], loan["dueDate"]))
    return results