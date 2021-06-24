from random import choice

from flask import Blueprint
from flask import session
from flask import jsonify

from app.card import calc_total
from app.card import get_display_card_name
from app.game import get_dummy_session

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


@bp.route("/status/<string:session_id>")
def status(session_id: str):
    game = session.get(session_id, None)
    if game is None:
        return jsonify({
            "game": "not found"
        })

    return jsonify({
        "you": {
            "total": calc_total(hand=[game['you']['hand'][0]]),
            "hand": [
                {
                    "alt": get_display_card_name(card=game['you']['hand'][0]),
                    "src": f"/static/card_img/{game['you']['hand'][0]}.png",
                }
            ]
        },
        "me": {
            "total": calc_total(hand=game['me']['hand']),
            "hand": [
                {
                    "alt": get_display_card_name(card=card_),
                    "src": f"/static/card_img/{card_}.png",
                } for card_ in game['me']['hand']
            ]
        }
    })


@bp.route("/hit/<string:session_id>")
def hit(session_id: str):
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

    # 변동사항 게임세션에 저장
    session[session_id] = game

    game_status = "ok"
    if calc_total(hand=game['me']['hand']) > 21:
        game_status = "bust with new card"

    return jsonify({
        "game": game_status,
        "you": you_hit,
        "me": {
            "alt": get_display_card_name(card=my_card),
            "src": f"/static/card_img/{my_card}.png",
            "total": calc_total(game['me']['hand'])
        }
    })


@bp.route("/stand/<string:session_id>")
def stand(session_id: str):
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

    # 게임 종료! - 세션 리셋하기
    session[session_id] = get_dummy_session()

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

    bootstrap_color = {
        True: "success",
        False: "danger"
    }.get(win, "secondary")

    return jsonify({
        "game": "end",
        "alert": {
            "head": head,
            "body": reason,
            "color": bootstrap_color
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
