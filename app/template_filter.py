from app.card import get_display_card_name as _get_display_card_name
from app.card import get_number as _get_number
from app.card import calc_total as _calc_total


def get_display_card_name(card: str) -> str:
    return _get_display_card_name(card=card)


def get_number(card: str) -> str:
    return str(_get_number(card=card))


def calc_total(hand: list) -> str:
    return str(_calc_total(hand=hand))


filter_list = [name for name in dir() if not name.startswith("_")]
