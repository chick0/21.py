def get_display_card_name(card: str) -> str:
    from .card import get_display_card_name
    return get_display_card_name(card=card)


def get_number(card: str) -> str:
    from .card import get_number
    return str(get_number(card=card))


def calc_total(hand: list) -> str:
    from .card import calc_total
    return str(calc_total(hand=hand))


def dk_body(dk: bool) -> str:
    if dk:
        return "bg-dark text-white-50"
    else:
        return ""


def dk_progress(dk: bool) -> str:
    if dk:
        return "progress-bar bg-secondary"
    else:
        return "progress-bar bg-info"
