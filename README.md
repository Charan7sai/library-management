# Library Management System (MongoDB)

A library management backend built with **MongoDB** and **Python (PyMongo)**. It supports book and member management, issuing and returning books, indexed search, and aggregation-based reports.

## Features
- CRUD for books and members
- Issue and return books with automatic availability tracking
- Fine calculation for overdue returns
- Text search by title, author or genre
- Aggregation reports: most borrowed books, books issued per month, overdue loans

## Tech Stack
- Database: MongoDB (Atlas / local)
- Language: Python 3.10
- Libraries: PyMongo, python-dotenv

## Schema Design

| Collection | Key fields | Design decision |
|---|---|---|
| `books` | isbn, title, author, genres[], totalCopies, availableCopies | `genres` is **embedded** because it is small and always read with the book |
| `members` | name, email, phone, membershipType, joinedOn | Standalone, since members exist independently of loans |
| `loans` | bookId, memberId, issuedOn, dueDate, returnedOn, fine | **Referenced** (stores IDs) because loans grow without limit and are queried on their own |

### Why embedding vs. referencing?
Genres are a small, fixed-size list that is always displayed with the book, so embedding avoids an extra query. Loans keep growing over time and are queried independently (overdue reports, member history), so embedding them in books or members would cause unbounded document growth. They are referenced instead.

## Why NoSQL?
- Flexible schema: new book attributes (edition, language, tags) can be added without migrations
- Embedded arrays (genres) model one-to-few relationships naturally
- Aggregation pipelines handle reporting without complex joins
- Easy horizontal scaling if the library grows

## Indexes
- Unique index on `books.isbn` and `members.email`
- Text index on `books.title` and `books.author`
- [ ] Add your `explain()` comparison here after Checkpoint 5

## Setup

```bash
git clone <your-repo-url>
cd library-management
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```
MONGO_URI=your_connection_string
DB_NAME=library
```

Test the connection:
```bash
python test_connection.py
```

## Usage
- [ ] Add commands for seeding data and running the app after Checkpoints 2-4

## Sample Queries and Reports
- [ ] Most borrowed books (Checkpoint 6)
- [ ] Overdue loans with member details (Checkpoint 6)

## Screenshots
- [ ] Compass view of collections
- [ ] `explain()` output with and without index
- [ ] Report outputs

## Future Improvements
- Web frontend (React or Flask templates)
- Authentication for librarians
- Email reminders for due dates