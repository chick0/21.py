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
        "K": 10,
    }.get(n)


def calc_total(hand: list) -> int:
    total, ace_count = calc_total_without_ace(hand=hand)
    ace_total = 0

    for i in range(0, ace_count):
        if ((21 - total - ace_total) - 11) >= 0:
            ace_total += 11
        else:
            ace_total += 1

    return total + ace_total


def calc_total_without_ace(hand: list) -> (int, int):
    total = 0
    ace_count = 0
    for card in hand:
        if not card.endswith("A"):
            total += get_number(card)
        else:
            ace_count += 1

    return total, ace_count
