from typing import List
from flask import render_template
from markupsafe import Markup


def get_markup(show_message: str, iclass="fas fa-cog"):
    return Markup(
        f"""<i class='{iclass}'></i>
        {show_message}."""
    )
