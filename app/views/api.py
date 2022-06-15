from random import choice

from flask import Blueprint
from flask import session
from flask import jsonify

from app import GAME_SESSION_ID
from app.card import calc_total
from app.card import get_display_card_name
from app.game import get_dummy_session
from app.winner import get_winner
from app.nickname import get_nickname

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


@bp.get("/joker")
def joker_pop():
    game = session.get(GAME_SESSION_ID, None)
    if game is None:
        return jsonify({
            "game": "not found"
        })

    joker = False
    if 'joker' in game['me']['hand']:
        del game['me']['hand'][game['me']['hand'].index('joker')]
        session[GAME_SESSION_ID] = game
        joker = True

    return jsonify({
        "game": "ok",
        "joker": joker,
        "total": calc_total(hand=game['me']['hand'])
    })


@bp.get("/status")
def status():
    game = session.get(GAME_SESSION_ID, None)
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
                    "src": game['you']['hand'][0],
                },
            ] + [
                {
                    "alt": "Hidden Card",
                    "src": "back",
                } for x in range(0, len(game['you']['hand']) - 1)
            ]
        },
        "me": {
            "total": calc_total(hand=game['me']['hand']),
            "hand": [
                {
                    "alt": get_display_card_name(card=card_),
                    "src": card_,
                } for card_ in game['me']['hand']
            ]
        }
    })


@bp.get("/hit")
def hit():
    game = session.get(GAME_SESSION_ID, None)
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
    session[GAME_SESSION_ID] = game

    game_status = "ok"
    if calc_total(hand=game['me']['hand']) > 21:
        game_status = "bust with new card"

    return jsonify({
        "game": game_status,
        "you": you_hit,
        "me": {
            "alt": get_display_card_name(card=my_card),
            "src": my_card,
            "total": calc_total(game['me']['hand'])
        }
    })


@bp.get("/stand")
def stand():
    game = session.get(GAME_SESSION_ID, None)
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

    win, reason = get_winner(
        you=calc_total(hand=game['you']['hand']),
        me=calc_total(hand=game['me']['hand']),
        name={
            "you": game['you']['name'],
            "me": game['me']['name']
        }
    )

    # 게임 종료! - 세션 리셋하기
    session[GAME_SESSION_ID] = get_dummy_session(
        your_name=get_nickname() if win is True else game['you']['name'],
        my_name=game['me']['name'],
        total=game['count']['total'] + 1,
        win=game['count']['win'] + 1 if win is True else game['count']['win']
    )

    return jsonify({
        "game": "end",
        "alert": {
            "head": {
                True: "승리!",
                False: "패배"
            }.get(win, "무승부"),
            "body": reason,
            "color": {
                True: "#15944A",
                False: "#DC143C"
            }.get(win, "#4D5459")
        },
        "you": {
            "total": calc_total(hand=game['you']['hand']),
            "hand": [
                {
                    "alt": get_display_card_name(card=card_),
                    "src": card_,
                } for card_ in game['you']['hand']
            ]
        },
        "count": session[GAME_SESSION_ID]['count'],
        "name": {
            # "me": session[GAME_SESSION_ID]['me']['name'],
            "you": session[GAME_SESSION_ID]['you']['name'],
        }
    })
