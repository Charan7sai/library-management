from db import db

def stats(label, cursor):
    s = cursor.explain()["executionStats"]
    print(f"{label}: docs examined = {s['totalDocsExamined']}, "
          f"returned = {s['nReturned']}, time = {s['executionTimeMillis']} ms")

# Genre query WITHOUT index (force a collection scan)
stats("Genre, no index", db.books.find({"genres": "Fiction"}).hint({"$natural": 1}))

# Genre query WITH index
stats("Genre, with index", db.books.find({"genres": "Fiction"}).hint("genres_idx"))