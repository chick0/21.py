
from flask import Blueprint
from flask import g
from flask import render_template

bp = Blueprint(
    name="offline",
    import_name="offline",
    url_prefix="/offline"
)


@bp.get("")
def page():
    g.use_meta = False
    return render_template(
        "offline/page.html"
    )
