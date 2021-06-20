def get_number(card: str) -> int:
    s, n = card
    return {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "X": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
    }.get(n)


def calc_total(hand: list) -> int:
    total = 0
    for card in hand:
        total += get_number(card)

    return total
