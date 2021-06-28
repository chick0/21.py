
from flask import Blueprint
from flask import session
from flask import render_template

from app import GAME_SESSION_ID
from app.game import get_dummy_session

bp = Blueprint(
    name="game",
    import_name="game",
    url_prefix="/game"
)


@bp.route("/table")
def table():
    game = session.get(GAME_SESSION_ID, None)
    if game is None:
        session[GAME_SESSION_ID] = get_dummy_session()
        game = session[GAME_SESSION_ID]

    return render_template(
        "game/table.html",
        game=game
    )
