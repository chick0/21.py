from secrets import token_bytes

from flask import Flask

from . import template_filter


GAME_SESSION_ID = "21"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_bytes(32)
    app.config['SESSION_COOKIE_NAME'] = "s"
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "Strict"

    # blueprint init
    from . import views
    for view in views.__all__:
        app.register_blueprint(getattr(getattr(getattr(__import__(f"app.views.{view}"), "views"), view), "bp"))

    # template filter init
    from . import template_filter
    for name in template_filter.filter_list:
        app.add_template_filter(f=getattr(template_filter, name), name=name)

    # register error handler
    from .error import error_map
    for code in error_map:
        app.register_error_handler(code, error_map[code])

    return app
