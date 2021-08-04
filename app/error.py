
from flask import redirect


def page_not_found(e):
    return redirect("/")


# error map
error_map = {
    404: page_not_found,
}
