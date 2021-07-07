from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")


class Game:
    start_cards = int(config.get("game", "start_cards", fallback=2))
    use_deck = int(config.get("game", "use_deck", fallback=2))
    use_nickname = config.get("game", "use_nickname", fallback=True)

    if isinstance(use_nickname, str):
        if use_nickname.lower() in ['true', 'yes', 'on']:
            use_nickname = True
        else:
            use_nickname = False


class Card:
    jack = int(config.get("card", "jack", fallback=10))
    queen = int(config.get("card", "queen", fallback=10))
    king = int(config.get("card", "king", fallback=10))


class Joker:
    effect = float(config.get("joker", "effect", fallback=0.5))
    cards = int(config.get("joker", "cards", fallback=1))

