from db import db

validators = {
    "books": {
        "bsonType": "object",
        "required": ["isbn", "title", "author", "genres", "totalCopies", "availableCopies"],
        "properties": {
            "isbn": {"bsonType": "string"},
            "title": {"bsonType": "string", "minLength": 1},
            "author": {"bsonType": "string", "minLength": 1},
            "genres": {"bsonType": "array", "items": {"bsonType": "string"}},
            "year": {"bsonType": "int"},
            "totalCopies": {"bsonType": "int", "minimum": 0},
            "availableCopies": {"bsonType": "int", "minimum": 0},
        },
    },
    "members": {
        "bsonType": "object",
        "required": ["name", "email", "membershipType", "joinedOn"],
        "properties": {
            "name": {"bsonType": "string", "minLength": 1},
            "email": {"bsonType": "string", "pattern": "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"},
            "phone": {"bsonType": "string"},
            "membershipType": {"enum": ["student", "faculty", "general"]},
            "joinedOn": {"bsonType": "date"},
        },
    },
    "loans": {
        "bsonType": "object",
        "required": ["bookId", "memberId", "issuedOn", "dueDate", "returnedOn", "fine"],
        "properties": {
            "bookId": {"bsonType": "objectId"},
            "memberId": {"bsonType": "objectId"},
            "issuedOn": {"bsonType": "date"},
            "dueDate": {"bsonType": "date"},
            "returnedOn": {"bsonType": ["date", "null"]},
            "fine": {"bsonType": ["int", "double"], "minimum": 0},
        },
    },
}

existing = db.list_collection_names()
for name, schema in validators.items():
    if name in existing:
        db.command("collMod", name, validator={"$jsonSchema": schema}, validationLevel="strict")
    else:
        db.create_collection(name, validator={"$jsonSchema": schema})
    print(f"Validator set on '{name}'")

db.books.create_index("isbn", unique=True)
db.members.create_index("email", unique=True)
db.loans.create_index("memberId")
db.loans.create_index("bookId")
print("Indexes created")