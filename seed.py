from datetime import datetime
from db import db

books_raw = [
    ("The Alchemist", "Paulo Coelho", ["Fiction", "Adventure"], 4),
    ("Wings of Fire", "A.P.J. Abdul Kalam", ["Biography"], 5),
    ("The Guide", "R.K. Narayan", ["Fiction"], 3),
    ("Malgudi Days", "R.K. Narayan", ["Fiction", "Short Stories"], 3),
    ("The White Tiger", "Aravind Adiga", ["Fiction"], 2),
    ("Sapiens", "Yuval Noah Harari", ["History", "Non-fiction"], 4),
    ("Atomic Habits", "James Clear", ["Self-help"], 6),
    ("Clean Code", "Robert C. Martin", ["Technology", "Programming"], 3),
    ("The Pragmatic Programmer", "Andrew Hunt", ["Technology", "Programming"], 2),
    ("Introduction to Algorithms", "Thomas H. Cormen", ["Technology", "Textbook"], 4),
    ("Database System Concepts", "Abraham Silberschatz", ["Technology", "Textbook"], 5),
    ("NoSQL Distilled", "Pramod Sadalage", ["Technology", "Database"], 2),
    ("MongoDB: The Definitive Guide", "Shannon Bradshaw", ["Technology", "Database"], 3),
    ("1984", "George Orwell", ["Fiction", "Dystopian"], 4),
    ("Animal Farm", "George Orwell", ["Fiction", "Satire"], 3),
    ("To Kill a Mockingbird", "Harper Lee", ["Fiction", "Classic"], 3),
    ("Pride and Prejudice", "Jane Austen", ["Fiction", "Romance", "Classic"], 2),
    ("The Hobbit", "J.R.R. Tolkien", ["Fiction", "Fantasy"], 4),
    ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", ["Fiction", "Fantasy"], 5),
    ("The Da Vinci Code", "Dan Brown", ["Fiction", "Mystery", "Thriller"], 3),
    ("Murder on the Orient Express", "Agatha Christie", ["Fiction", "Mystery"], 2),
    ("The Hound of the Baskervilles", "Arthur Conan Doyle", ["Fiction", "Mystery"], 2),
    ("A Brief History of Time", "Stephen Hawking", ["Science", "Non-fiction"], 3),
    ("Cosmos", "Carl Sagan", ["Science", "Non-fiction"], 2),
    ("The Selfish Gene", "Richard Dawkins", ["Science"], 2),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", ["Finance", "Self-help"], 4),
    ("The Discovery of India", "Jawaharlal Nehru", ["History", "Non-fiction"], 2),
    ("Train to Pakistan", "Khushwant Singh", ["Fiction", "History"], 2),
    ("The God of Small Things", "Arundhati Roy", ["Fiction"], 2),
    ("Python Crash Course", "Eric Matthes", ["Technology", "Programming"], 4),
]

books = []
for i, (title, author, genres, copies) in enumerate(books_raw, start=1):
    books.append({
        "isbn": f"978-1-0000-{i:04d}-0",
        "title": title,
        "author": author,
        "genres": genres,
        "year": 2000 + (i % 24),
        "totalCopies": copies,
        "availableCopies": copies,
    })

members_raw = [
    ("Aarav Sharma", "aarav@example.com", "9000000001", "student"),
    ("Diya Patel", "diya@example.com", "9000000002", "student"),
    ("Rohan Verma", "rohan@example.com", "9000000003", "student"),
    ("Ananya Singh", "ananya@example.com", "9000000004", "student"),
    ("Kabir Mehta", "kabir@example.com", "9000000005", "general"),
    ("Isha Gupta", "isha@example.com", "9000000006", "general"),
    ("Dr. Meera Nair", "meera@example.com", "9000000007", "faculty"),
    ("Prof. Arjun Rao", "arjun@example.com", "9000000008", "faculty"),
    ("Saanvi Joshi", "saanvi@example.com", "9000000009", "student"),
    ("Vihaan Kapoor", "vihaan@example.com", "9000000010", "general"),
]

members = [
    {"name": n, "email": e, "phone": p, "membershipType": t, "joinedOn": datetime(2026, 1, 1)}
    for n, e, p, t in members_raw
]

db.loans.delete_many({})
db.books.delete_many({})
db.members.delete_many({})

print("Inserted books:", len(db.books.insert_many(books).inserted_ids))
print("Inserted members:", len(db.members.insert_many(members).inserted_ids))