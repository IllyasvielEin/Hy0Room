from flask import Blueprint, render_template, request, session, redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    username = session.get('username')
    if username is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for("channels.get_channels"))
