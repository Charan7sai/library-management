import re
from db import db


def text_search(query, limit=10):
    """Word-based search on title and author, ranked by relevance."""
    return list(
        db.books.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}, "title": 1, "author": 1, "genres": 1},
        ).sort([("score", {"$meta": "textScore"})]).limit(limit)
    )


def search_by_genre(genre):
    return list(db.books.find({"genres": genre}, {"title": 1, "author": 1, "genres": 1}))


def search_by_author(author):
    """Partial, case-insensitive match (uses regex, so no text index)."""
    pattern = re.escape(author)
    return list(db.books.find({"author": {"$regex": pattern, "$options": "i"}},
                              {"title": 1, "author": 1}))