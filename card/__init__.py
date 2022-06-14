from os import listdir
from os.path import join
from os.path import abspath
from os.path import dirname
from base64 import b64encode
from hashlib import sha384

from flask import current_app

PATH = dirname(abspath(__file__))


def get_card_ids() -> list:
    return [x.replace(".png", "") for x in listdir(PATH) if x.endswith(".png")]


def read_card(card_id: str) -> str:
    with open(join(PATH, card_id + ".png"), mode="rb") as fp:
        card = fp.read()

    return "data:image/png;base64," + b64encode(card).decode()


def get_cards() -> dict:
    cards = {}
    for card_id in get_card_ids():
        card = read_card(card_id=card_id)
        cards[card_id] = card

    return cards


def get_card_version(cards: dict) -> str:
    b = ""
    for card in cards.values():
        b += card

    return sha384(b.encode()).hexdigest()


def get_from_config() -> tuple[str, dict]:
    app = current_app

    version: str = app.config['21_CARD_VERSION']
    cards: dict = app.config['21_CARDS']

    return (
        version,
        cards
    )
