from random import shuffle

from .nickname import get_nickname


def get_card_deck() -> list:
    return [
        "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CX", "CJ", "CQ", "CK",
        "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DX", "DJ", "DQ", "DK",
        "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "HX", "HJ", "HQ", "HK",
        "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "SX", "SJ", "SQ", "SK",
    ] * 2


def get_dummy_session(your_name: str = get_nickname(), my_name: str = get_nickname()) -> dict:
    card = get_card_deck()
    shuffle(card)

    you, me = [], []

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
        }
    }
