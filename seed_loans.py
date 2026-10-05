import random
from datetime import datetime, timedelta
from db import db

random.seed(42)
books = list(db.books.find({}, {"_id": 1}))
members = list(db.members.find({}, {"_id": 1}))

db.loans.delete_many({})
# reset availability before recalculating
db.books.update_many({}, [{"$set": {"availableCopies": "$totalCopies"}}])

loans = []
now = datetime.now()
for _ in range(60):
    book = random.choice(books)
    member = random.choice(members)
    issued = now - timedelta(days=random.randint(1, 150))
    due = issued + timedelta(days=14)
    returned = None
    fine = 0
    if random.random() < 0.7:  # 70% already returned
        returned = issued + timedelta(days=random.randint(3, 25))
        fine = max(0, (returned.date() - due.date()).days) * 2
    loans.append({
        "bookId": book["_id"], "memberId": member["_id"],
        "issuedOn": issued, "dueDate": due,
        "returnedOn": returned, "fine": fine,
    })

db.loans.insert_many(loans)

# Keep availableCopies consistent with active loans (never below 0)
for loan in loans:
    if loan["returnedOn"] is None:
        db.books.update_one(
            {"_id": loan["bookId"], "availableCopies": {"$gt": 0}},
            {"$inc": {"availableCopies": -1}},
        )
print("Inserted", len(loans), "loans")