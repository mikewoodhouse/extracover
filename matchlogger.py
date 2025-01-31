import sqlite3

from nicegui import app, ui

from matchday.common.db import books_db_path
from matchday.data import BookRepository
from matchday.models import Book
from matchday.views import BookBuilderView, InplayView

"""
Are separate pages necessary?
Given a large screen, could all the needed views be presented in one page?
"""


@ui.page("/")
def navigation():
    ui.link("Match Setup", match_view)
    ui.link("Inplay/Logger", inplay_view)


@ui.page("/setup/{book_id}")
def match_view(book_id: int | None):
    conn = sqlite3.connect(books_db_path)
    repo = BookRepository(conn)
    book: Book = repo.get(book_id)
    app.storage.user.pop("book_id")
    view = BookBuilderView(repo, book)
    view.show()


@ui.page("/match/{match_id}")
def inplay_view(match_id: int | None):
    view = InplayView()
    view.show()


ui.run(storage_secret="banana", dark=True, favicon="🏏", title="ExtraCover")
