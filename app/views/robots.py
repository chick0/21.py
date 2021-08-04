
from flask import Blueprint
from flask import Response


bp = Blueprint(
    name="robots",
    import_name="robots",
    url_prefix="/"
)


@bp.route("/robots.txt")
def txt():
    return Response(
        "\n".join([
            'User-agent: *',
            'Allow: /$',
            'Allow: /rule',
            'Disallow: /'
        ]),
        mimetype="text/plain"
    )
