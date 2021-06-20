
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import render_template

bp = Blueprint(
    name="lobby",
    import_name="lobby",
    url_prefix="/"
)


@bp.route("/")
def index():
    return redirect(url_for("game.new_game"))
    # return "lobby.index"
