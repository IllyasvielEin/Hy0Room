from flask import Blueprint, render_template, request, session, redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for("channels.get_channels"))