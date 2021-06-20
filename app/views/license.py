
from flask import Blueprint
from flask import render_template

bp = Blueprint(
    name="license",
    import_name="license",
    url_prefix="/license"
)


@bp.route("")
def page():
    return render_template(
        "license/page.html"
    )
