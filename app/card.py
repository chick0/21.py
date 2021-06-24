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
        "J": 10,
        "Q": 10,
        "K": 11,
    }.get(n)


def calc_total(hand: list) -> int:
    total = 0
    total_without = calc_total_without_ace(hand=hand)
    for card in hand:
        if not card.endswith("A"):
            total += get_number(card)
        else:
            if total_without <= 10:
                total += 11
            else:
                total += 1

    return total


def calc_total_without_ace(hand: list) -> int:
    total = 0
    for card in hand:
        if not card.endswith("A"):
            total += get_number(card)

    return total
