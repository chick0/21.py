
from flask import Blueprint
from flask import render_template

bp = Blueprint(
    name="offline",
    import_name="offline",
    url_prefix="/offline"
)


@bp.get("")
def page():
    return render_template(
        "offline/page.html"
    )
