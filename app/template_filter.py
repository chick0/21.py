def get_display_card_name(card: str) -> str:
    s, n = card
    s = {
        "C": "Clubs",
        "D": "Diamonds",
        "H": "Hearts",
        "S": "Spaces"
    }.get(s)

    n = {
        "X": "10",

        "A": "Ace",
        "J": "Jack",
        "Q": "Queen",
        "K": "King",
    }.get(n, n)

    return f"{s} {n}"


def get_number(card: str) -> str:
    from .card import get_number
    return str(get_number(card=card))


def calc_total(hand: list) -> str:
    from .card import calc_total
    return str(calc_total(hand=hand))
