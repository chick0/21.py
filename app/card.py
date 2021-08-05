
from .config import Card
from .config import Joker


def get_display_card_name(card: str) -> str:
    try:
        s, n = card
    except ValueError:
        # too many values to unpack
        return "Joker"

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


def get_number(card: str) -> int:
    s, n = card
    return {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "X": 10,
        "J": Card.jack,
        "Q": Card.queen,
        "K": Card.king,
    }.get(n, 0)


def calc_total(hand: list) -> int:
    total, ace_count, joker = calc_total_without_ace(hand=hand)
    ace_total = 0

    for i in range(0, ace_count):
        if ((21 - total - ace_total) - 11) >= 0:
            ace_total += 11
        else:
            ace_total += 1

    return total + ace_total if joker is False else int((total + ace_total) * Joker.effect)


def calc_total_without_ace(hand: list) -> (int, int, bool):
    total = 0
    ace_count = 0
    joker = False

    for card in hand:
        if card == "joker":
            joker = True
        elif not card.endswith("A"):
            total += get_number(card)
        else:
            ace_count += 1

    return total, ace_count, joker
