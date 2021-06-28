from secrets import token_bytes

from flask import Flask
from flask import Response

from . import template_filter


GAME_SESSION_ID = "21"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_bytes(32)
    app.config['SESSION_COOKIE_NAME'] = "s"
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "Strict"

    app.add_template_filter(template_filter.get_display_card_name, "get_display_card_name")
    app.add_template_filter(template_filter.get_number, "get_number")
    app.add_template_filter(template_filter.calc_total, "calc_total")

    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(views, view).__getattribute__("bp"))

    @app.after_request
    def set_header(response):
        response.headers['X-Frame-Options'] = "deny"
        response.headers['X-Powered-By'] = "chick_0"
        return response

    @app.route("/robots.txt")
    def robots_txt():
        return Response(
            "\n".join([
                'User-agent: *',
                'Allow: /$',
                'Disallow: /'
            ]),
            mimetype="text/plain"
        )

    return app
