from json import dumps

from flask import Blueprint
from flask import session
from flask import render_template

from app.config import Game
from app.config import Card
from app.config import Joker

from app import GAME_SESSION_ID
from app.game import get_dummy_session
from card import get_from_config

bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("")
def index():
    game = session.get(GAME_SESSION_ID, None)
    if game is None:
        session[GAME_SESSION_ID] = get_dummy_session()
        game = session[GAME_SESSION_ID]

    version, cards = get_from_config()

    return render_template(
        "index.html",
        game=game,
        version=version,
        cards=dumps(cards),
        cards_obj=cards,

        start_cards=Game.start_cards,
        use_deck=Game.use_deck,
        jack=Card.jack,
        queen=Card.queen,
        king=Card.king,
        card=Card,
        joker=Joker,
    )
