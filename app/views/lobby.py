
from flask import Blueprint
from flask import render_template

from app.config import Game
from app.config import Card
from app.config import Joker


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
    return render_template(
        "lobby/rule.html",
        start_cards=Game.start_cards,
        use_deck=Game.use_deck,
        jack=Card.jack,
        queen=Card.queen,
        king=Card.king,
        effect=Joker.effect,
        cards=Joker.cards
    )
