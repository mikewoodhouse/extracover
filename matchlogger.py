from nicegui import app, ui

from matchday.views import BookBuilderView, InplayView

"""
Are separate pages necessary?
Given a large screen, could all the needed views be presented in one page?
"""


@ui.page("/")
def navigation():
    ui.link("Match Setup", match_view)
    ui.link("Inplay/Logger", inplay_view)


@ui.page("/setup")
def match_view():
    app.storage.user.pop("book_id")
    view = BookBuilderView()
    view.show()


@ui.page("/match/{match_id}")
def inplay_view(match_id: int | None):
    view = InplayView()
    view.show()


ui.run(storage_secret="banana", dark=True, favicon="🏏", title="ExtraCover")
