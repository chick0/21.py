
from flask import Blueprint
from flask import session
from flask import jsonify
from flask import redirect
from flask import url_for

from app.card import calc_total
from app.card import get_display_card_name

bp = Blueprint(
    name="api",
    import_name="api",
    url_prefix="/api"
)


@bp.route("/hit/<string:session_id>")
def hit(session_id):
    game = session.get(session_id, None)
    if game is None or game['playing'] is False:
        return jsonify({
            "game": "not found"
        })

    you_hit = False
    if calc_total(hand=game['you']['hand']) < 16:
        your_card = game['card'].pop()
        game['you']['hand'].append(your_card)

        you_hit = True
        del your_card

    my_card = game['card'].pop()
    game['me']['hand'].append(my_card)

    "hit!"
    session[session_id] = game

    if calc_total(hand=game['me']['hand']) > 21:
        return jsonify({
            "game": "bust"
        })

    return jsonify({
        "game": "ok",
        "new_card": {
            "you": you_hit,
            "me": {
                "alt": get_display_card_name(card=my_card),
                "src": f"/static/card_img/{my_card}.png",
                "total": calc_total(game['me']['hand'])
            }
        }
    })


@bp.route("/stand/<string:session_id>")
def stand(session_id):
    game = session.get(session_id, None)
    if game is None or game['playing'] is False:
        return redirect(url_for("lobby.index", game="not-found"))

    while True:
        if calc_total(hand=game['you']['hand']) < 16:
            your_card = game['card'].pop()
            game['you']['hand'].append(your_card)
            del your_card
        else:
            break

    # game is end!
    game['playing'] = False

    "stand!"
    session[session_id] = game

    return redirect(url_for("game.end", session_id=session_id))
