import reports

def section(title):
    print(f"\n=== {title} ===")

section("Most borrowed books")
for r in reports.most_borrowed_books():
    print(f"{r['title']} by {r['author']}: {r['timesBorrowed']} loans")

section("Books issued per month")
for r in reports.books_issued_per_month():
    print(f"{r['month']}: {r['booksIssued']}")

section("Overdue loans")
for r in reports.overdue_loans():
    print(f"{r['title']} | {r['member']} ({r['email']}) | {r['daysOverdue']} days overdue")

section("Top borrowers")
for r in reports.top_borrowers():
    print(f"{r['name']}: {r['loans']} loans, fines ₹{r['totalFines']}")

section("History for aarav@example.com")
for r in reports.member_history("aarav@example.com"):
    status = r["returnedOn"].strftime("%d-%m-%Y") if r["returnedOn"] else "NOT RETURNED"
    print(f"{r['title']} | issued {r['issuedOn'].strftime('%d-%m-%Y')} | returned {status} | fine ₹{r['fine']}")