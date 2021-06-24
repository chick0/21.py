from uuid import uuid4

from flask import Blueprint
from flask import session
from flask import url_for
from flask import redirect
from flask import render_template

from app.game import get_dummy_session

bp = Blueprint(
    name="game",
    import_name="game",
    url_prefix="/game"
)


@bp.route("/new")
def new_game():
    session_id = str(uuid4())
    session[session_id] = get_dummy_session()

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
