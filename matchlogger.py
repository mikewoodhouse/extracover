import sqlite3

from nicegui import app, ui

from matchday.common.db import books_db_path
from matchday.data import BookRepository
from matchday.models import Book
from matchday.viewmodels import BookBuilder, InplayManager
from matchday.views import BookSetupView, InplayView

"""
Are separate pages necessary?
Given a large screen, could all the needed views be presented in one page?
"""


@ui.page("/")
def navigation():
    ui.link("Match Setup", "/setup")
    ui.link("Inplay/Logger", inplay_view)


@ui.page("/setup")
def match_view(book_id: int | None = None):
    conn = sqlite3.connect(books_db_path)
    repo = BookRepository(conn)
    book: Book = repo.get(book_id) if book_id else Book()
    book_builder = BookBuilder(book=book, repo=repo)
    app.storage.user.pop("book_id")
    view = BookSetupView(book_builder)
    view.show()


@ui.page("/match")
def inplay_view(match_id: int | None):
    conn = sqlite3.connect(books_db_path)
    repo = BookRepository(conn)
    book: Book = repo.get(match_id) if match_id else Book()
    manager = InplayManager(book)
    view = InplayView(manager)
    view.show()


ui.run(storage_secret="banana", dark=True, favicon="🏏", title="ExtraCover")
