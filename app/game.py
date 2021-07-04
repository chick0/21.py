from random import shuffle

from .nickname import get_nickname


def get_card_deck() -> list:
    return [
        "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CX", "CJ", "CQ", "CK",
        "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DX", "DJ", "DQ", "DK",
        "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "HX", "HJ", "HQ", "HK",
        "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "SX", "SJ", "SQ", "SK",
    ] * 2 + ["joker"]


def get_dummy_session(your_name: str = None, my_name: str = None, total: int = 0, win: int = 0) -> dict:
    if your_name is None:
        your_name = get_nickname()

    if my_name is None:
        my_name = get_nickname()

    card = get_card_deck()
    shuffle(card)

    you, me = [], []

    you.append(card.pop())
    me.append(card.pop())
    you.append(card.pop())
    me.append(card.pop())

    return {
        "card": card,
        "you": {
            "name": your_name,
            "hand": you,
            "stand": False
        },
        "me": {
            "name": my_name,
            "hand": me,
        },
        "count": {
            "total": total,
            "win": win,
            "lose_or_draw": total - win,
            "winning_rate": round((win / total) * 100) if total != 0 else 0,
        }
    }
