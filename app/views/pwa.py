
from flask import Blueprint
from flask import send_file

bp = Blueprint(
    name="pwa",
    import_name="pwa",
    url_prefix="/"
)


@bp.route("/sw.js")
def sw():
    return send_file(
        "pwa/sw.js",
        mimetype="application/javascript"
    )


@bp.route("/manifest.json")
def manifest():
    return send_file(
        "pwa/manifest.json",
        mimetype="application/json"
    )
