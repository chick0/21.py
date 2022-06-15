from secrets import token_bytes

from flask import Flask
from flask import Response
from flask import redirect

from card import get_cards
from card import get_card_version

GAME_SESSION_ID = "21"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_bytes(32)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "Strict"

    cards = get_cards()
    app.config['21_CARDS'] = cards
    app.config['21_CARD_VERSION'] = get_card_version(cards=cards)

    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(views, view), "bp"))

    from . import template_filter
    for name in template_filter.filter_list:
        app.add_template_filter(f=getattr(template_filter, name), name=name)

    app.register_error_handler(
        code_or_exception=404,
        f=lambda x: redirect("/")
    )

    @app.get("/robots.txt")
    def txt():
        return Response(
            "\n".join([
                'User-agent: *',
                'Allow: /'
            ]),
            mimetype="text/plain"
        )

    return app
