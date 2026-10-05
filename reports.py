from datetime import datetime
from db import db


def most_borrowed_books(limit=5):
    return list(db.loans.aggregate([
        {"$group": {"_id": "$bookId", "timesBorrowed": {"$sum": 1}}},
        {"$sort": {"timesBorrowed": -1}},
        {"$limit": limit},
        {"$lookup": {"from": "books", "localField": "_id",
                     "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$project": {"_id": 0, "title": "$book.title",
                      "author": "$book.author", "timesBorrowed": 1}},
    ]))


def books_issued_per_month():
    return list(db.loans.aggregate([
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m", "date": "$issuedOn"}},
                    "booksIssued": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
        {"$project": {"_id": 0, "month": "$_id", "booksIssued": 1}},
    ]))


def overdue_loans():
    now = datetime.now()
    return list(db.loans.aggregate([
        {"$match": {"returnedOn": None, "dueDate": {"$lt": now}}},
        {"$lookup": {"from": "books", "localField": "bookId",
                     "foreignField": "_id", "as": "book"}},
        {"$lookup": {"from": "members", "localField": "memberId",
                     "foreignField": "_id", "as": "member"}},
        {"$unwind": "$book"},
        {"$unwind": "$member"},
        {"$project": {
            "_id": 0, "title": "$book.title", "member": "$member.name",
            "email": "$member.email", "dueDate": 1,
            "daysOverdue": {"$dateDiff": {"startDate": "$dueDate", "endDate": now, "unit": "day"}},
        }},
        {"$sort": {"daysOverdue": -1}},
    ]))


def member_history(email):
    member = db.members.find_one({"email": email})
    if not member:
        raise ValueError("Member not found")
    return list(db.loans.aggregate([
        {"$match": {"memberId": member["_id"]}},
        {"$lookup": {"from": "books", "localField": "bookId",
                     "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$sort": {"issuedOn": -1}},
        {"$project": {"_id": 0, "title": "$book.title", "issuedOn": 1,
                      "returnedOn": 1, "fine": 1}},
    ]))


def top_borrowers(limit=3):
    return list(db.loans.aggregate([
        {"$group": {"_id": "$memberId", "loans": {"$sum": 1}, "totalFines": {"$sum": "$fine"}}},
        {"$sort": {"loans": -1}},
        {"$limit": limit},
        {"$lookup": {"from": "members", "localField": "_id",
                     "foreignField": "_id", "as": "member"}},
        {"$unwind": "$member"},
        {"$project": {"_id": 0, "name": "$member.name", "loans": 1, "totalFines": 1}},
    ]))