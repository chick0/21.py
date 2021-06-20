
from flask import Blueprint

bp = Blueprint(
    name="docs",
    import_name="docs",
    url_prefix="/docs"
)


@bp.route("/")
def index():
    return "docs.index"
