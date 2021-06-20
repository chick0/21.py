from uuid import uuid4
from random import shuffle

from flask import Blueprint
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import render_template

from app.nickname import get_nickname
from app.card import calc_total

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
        "playing": True,
        "card": card,
        "you": {
            "name": get_nickname(),
            "hand": [computer],
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

    if game['playing'] is False:
        return redirect(url_for("game.end", session_id=session_id))

    do = request.args.get("do")
    if do == "hit":
        if calc_total(hand=game['you']['hand']) < 16:
            your_card = game['card'].pop()
            game['you']['hand'].append(your_card)
            del your_card

        my_card = game['card'].pop()
        game['me']['hand'].append(my_card)
        del my_card

        "hit!"
        session[session_id] = game

        if calc_total(hand=game['me']['hand']) > 21:
            return redirect(url_for("game.table", session_id=session_id, do="stand"))
    elif do == "stand":
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

    return render_template(
        "game/table.html",
        game=game
    )


@bp.route("/<string:session_id>/end")
def end(session_id: str):
    game = session.get(session_id, None)
    if game is None:
        return redirect(url_for("game.new_game"))

    if game['playing'] is True:
        return redirect(url_for("game.table", session_id=session_id))

    you = calc_total(hand=game['you']['hand'])
    me = calc_total(hand=game['me']['hand'])

    if me == 21:
        win = True
        reason = "축하드립니다! 21을 만들었습니다!"
    elif you == 21:
        win = False
        reason = f"이런! <b>{game['you']['name']}</b>(이)가 21을 만들었습니다!"
    elif me > 21:
        win = False
        reason = "이런! 당신의 숫자 합이 21보다 크네요..."
    elif you > 21:
        win = True
        reason = f"우와! <b>{game['you']['name']}</b>(이)의 숫자 합이 21보다 크네요"
    elif me < you:
        win = False
        reason = f"이런! 당신의 숫자합이 <b>{game['you']['name']}</b>(이)의 숫자 합 보다 작네요..."
    elif me > you:
        win = True
        reason = f"축하드립니다! <b>{game['you']['name']}</b>(이) 보다 큰 숫자를 만들었습니다!"
    else:
        win = None
        reason = "무승부..."

    del session[session_id]
    return render_template(
        "game/end.html",
        game=game,

        win=win,
        reason=reason
    )
