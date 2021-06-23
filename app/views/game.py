from uuid import uuid4
from random import shuffle

from flask import Blueprint
from flask import session
from flask import url_for
from flask import redirect
from flask import render_template

from app.nickname import get_nickname

bp = Blueprint(
    name="game",
    import_name="game",
    url_prefix="/game"
)


@bp.route("/new")
def new_game():
    card = [
        "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CX", "CJ", "CQ", "CK",
        "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DX", "DJ", "DQ", "DK",
        "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "HX", "HJ", "HQ", "HK",
        "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "SX", "SJ", "SQ", "SK",
    ] * 2

    shuffle(card)

    computer = card.pop()
    me = card.pop()

    session_id = str(uuid4())
    session[session_id] = {
        "card": card,
        "you": {
            "name": get_nickname(),
            "hand": [computer],
            "stand": False
        },
        "me": {
            "name": get_nickname(),
            "hand": [me],
        }
    }

    return redirect(url_for("game.table", session_id=session_id))


@bp.route("/<string:session_id>")
def table(session_id):
    game = session.get(session_id, None)
    if game is None:
        return redirect(url_for("game.new_game"))

    return render_template(
        "game/table.html",
        game=game,
        session_id=session_id
    )
