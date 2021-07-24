from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask import redirect

from app import DARK_MODE_COOKIE

bp = Blueprint(
    name="dark",
    import_name="dark",
    url_prefix="/dark"
)


@bp.get("/toggle")
def toggle():
    target = request.referrer
    if target is None:
        target = "/"

    resp = redirect(target)

    if request.cookies.get(DARK_MODE_COOKIE, "undefined") == "on":
        resp.set_cookie(
            key="dk",
            value="off"
        )
    else:
        resp.set_cookie(
            key="dk",
            value="on",
            expires=datetime.now() + timedelta(hours=12)
        )

    return resp
