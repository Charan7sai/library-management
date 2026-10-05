# Library Management System (MongoDB + Python)

A command-line library management system built with **MongoDB** and **Python (PyMongo)**. It manages books and members, issues and returns books with automatic fine calculation, supports indexed search, and produces reports using aggregation pipelines.

## Features
- CRUD for books and members, with duplicate and invalid data rejected
- Issue and return books with live availability tracking
- Loan rules: 14-day loan period, ₹2/day fine, max 3 active loans per member
- Search by title/author (text index), genre (multikey index) and partial author name (regex)
- Aggregation reports: most borrowed books, books issued per month, overdue loans, top borrowers, member borrowing history

## Tech Stack
- **Database:** MongoDB 5.0+ (Atlas or local)
- **Language:** Python 3.10
- **Libraries:** PyMongo, python-dotenv

## Schema Design

| Collection | Key fields | Design decision |
|---|---|---|
| `books` | isbn, title, author, genres[], year, totalCopies, availableCopies | `genres` is **embedded** because it is small and always read with the book |
| `members` | name, email, phone, membershipType, joinedOn | Standalone, since members exist independently of loans |
| `loans` | bookId, memberId, issuedOn, dueDate, returnedOn, fine | **Referenced** (stores IDs) because loans grow without limit and are queried on their own |

### Embedding vs. referencing
Genres are a small list that is always displayed with the book, so embedding avoids an extra query. Loans keep growing and are queried independently (overdue reports, member history), so embedding them inside books or members would cause unbounded document growth. They are referenced instead and joined with `$lookup` when needed.

## Why NoSQL?
- **Flexible schema:** new book attributes (edition, language, tags) can be added without migrations
- **Embedded arrays** model one-to-few relationships (book to genres) naturally
- **Aggregation pipelines** handle reporting without complex multi-table JOINs
- **Horizontal scaling** is available if the library grows

## Data Validation
Validation lives in the database itself using `$jsonSchema`, so even a buggy script cannot insert bad data.
- Required fields on every collection
- `totalCopies` and `availableCopies` must be integers >= 0
- Email must match a valid pattern
- `membershipType` must be one of `student`, `faculty`, `general`
- Unique indexes on `books.isbn` and `members.email`

## Indexes
| Index | Purpose |
|---|---|
| `books.isbn` (unique) | Prevent duplicate books, fast lookup by ISBN |
| `members.email` (unique) | Prevent duplicate members, fast lookup by email |
| `books` text index on `title`, `author` | Ranked word search |
| `books.genres` | Fast genre filtering |
| `loans.memberId`, `loans.bookId` | Fast joins and history lookups |


## Issue and Return Logic
- Issuing uses `find_one_and_update` with the condition `availableCopies > 0`. This is **atomic**, so two members can never take the last copy.
- On a replica set (such as Atlas), the loan insert and the copy decrement run inside a **multi-document transaction**. On a standalone server, the code falls back to atomic updates with a manual rollback.
- Returns filter on `returnedOn: null`, which prevents returning the same loan twice.
- Books and members with active loans cannot be deleted.
- Changing `totalCopies` adjusts `availableCopies` by the same amount, so the counts never drift apart.

## Project Structure
```
db.py            connection helper and transaction detection
setup_db.py      validators and indexes
seed.py          sample books and members
seed_loans.py    sample loan history for reports
crud.py          book and member CRUD
loans.py         issue/return logic, fines, transactions
search.py        text, genre and author search
reports.py       aggregation reports
run_reports.py   prints all reports
explain_demo.py  index vs. no-index comparison
cli.py           terminal menu
test_validation.py, test_loans.py   automated checks
```

## Setup

```bash
git clone https://github.com/Charan7sai/library-management.git
cd library-management
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
MONGO_URI=your_connection_string
DB_NAME=library
```
Use `mongodb://localhost:27017` for a local server, or your Atlas connection string.

Initialise the database (run once, in this order):
```bash
python setup_db.py      # validators and indexes
python seed.py          # 30 books and 10 members
python seed_loans.py    # 60 sample loans
```

## Usage

Start the menu:
```bash
python cli.py
```

| Option | Action |
|---|---|
| 1-5 | Add, view, list, update, delete books |
| 6-10 | Add, view, list, update, delete members |
| 11 | Issue a book |
| 12 | Return a book |
| 13 | Member's active loans |
| 14 | Search by title/author |
| 15 | Search by genre |
| 16 | Reports (popular and overdue) |

Print all reports:
```bash
python run_reports.py
```

## Reports

All reports are aggregation pipelines in `reports.py`.

| Report | Stages used |
|---|---|
| Most borrowed books | `$group`, `$sort`, `$limit`, `$lookup`, `$unwind`, `$project` |
| Books issued per month | `$group` with `$dateToString`, `$sort`, `$project` |
| Overdue loans | `$match`, two `$lookup`s (books and members), `$unwind`, `$project` with `$dateDiff`, `$sort` |
| Top borrowers | `$group`, `$sort`, `$limit`, `$lookup`, `$project` |
| Member history | `$match`, `$lookup`, `$unwind`, `$sort`, `$project` |

Example, the overdue loans pipeline:
```python
{"$match": {"returnedOn": None, "dueDate": {"$lt": now}}},
{"$lookup": {"from": "books", "localField": "bookId", "foreignField": "_id", "as": "book"}},
{"$lookup": {"from": "members", "localField": "memberId", "foreignField": "_id", "as": "member"}},
{"$unwind": "$book"},
{"$unwind": "$member"},
{"$project": {"title": "$book.title", "member": "$member.name",
              "daysOverdue": {"$dateDiff": {"startDate": "$dueDate", "endDate": now, "unit": "day"}}}}
```
These pipelines replace the multi-table JOINs a SQL design would need.

## Testing
```bash
python test_validation.py   # bad data must be rejected
python test_loans.py        # issue, return, fine, double return, zero copies
```
`test_loans.py` clears the `loans` collection, so rerun `seed.py` and `seed_loans.py` afterwards.

## Future Improvements
- Web frontend (Flask or React)
- Librarian authentication
- Email reminders for due dates
- Reservation queue for books with no copies available