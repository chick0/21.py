from random import choice

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


def hit_or_stand(total: int) -> bool:
    if total <= 14:
        return True
    elif total >= 17:
        return False
    else:
        do_hit = [True] * 21

        if total > 21:
            total = 21

        for i in range(0, total):
            do_hit[i] = False

        return choice(do_hit)


@bp.route("/hit/<string:session_id>")
def hit(session_id):
    game = session.get(session_id, None)
    if game is None:
        return jsonify({
            "game": "not found"
        })

    if calc_total(hand=game['me']['hand']) >= 21:
        return jsonify({
            "game": "bust"
        })

    you_hit = False
    if hit_or_stand(total=calc_total(hand=game['you']['hand'])) and game['you']['stand'] is False:
        your_card = game['card'].pop()
        game['you']['hand'].append(your_card)

        you_hit = True
        del your_card
    else:
        game['you']['stand'] = True

    my_card = game['card'].pop()
    game['me']['hand'].append(my_card)

    "hit!"
    session[session_id] = game

    if calc_total(hand=game['me']['hand']) > 21:
        return jsonify({
            "game": "bust with new card",
            "new_card": {
                "you": you_hit,
                "me": {
                    "alt": get_display_card_name(card=my_card),
                    "src": f"/static/card_img/{my_card}.png",
                    "total": calc_total(game['me']['hand'])
                }
            }
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
    if game is None:
        return jsonify({
            "game": "not found"
        })

    while True:
        if hit_or_stand(total=calc_total(hand=game['you']['hand'])) and game['you']['stand'] is False:
            your_card = game['card'].pop()
            game['you']['hand'].append(your_card)
            del your_card
        else:
            break

    "stand!"

    # game is end!
    del session[session_id]

    # # # # # # # # # # # # # # # # # # # # # # #

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
        reason = ""

    head = {
        True: "승리!",
        False: "패배..."
    }.get(win, "무승부")

    alert_class = {
        True: "alert-success",
        False: "alert-danger"
    }.get(win, "alert-secondary")

    print(game['me']['hand'])

    return jsonify({
        "game": "end",
        "alert": {
            "head": head,
            "body": reason,
            "class": f"alert {alert_class}"
        },
        "you": {
            "total": you,
            "hand": [
                {
                    "alt": get_display_card_name(card=card_),
                    "src": f"/static/card_img/{card_}.png",
                } for card_ in game['you']['hand']
            ]
        }
    })
