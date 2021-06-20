
from flask import Blueprint
from flask import render_template

bp = Blueprint(
    name="lobby",
    import_name="lobby",
    url_prefix="/"
)


@bp.route("/")
def index():
    return render_template(
        "lobby/index.html"
    )


@bp.route("/rule")
def rule():
    return "lobby.rule"
