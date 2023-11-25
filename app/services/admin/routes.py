from flask import Blueprint, session, request, render_template, redirect, url_for, current_app, flash, jsonify

from app.hyldb.handler.users import UserHandler
from app.hyldb.handler.channels import ChannelsHandler
from app.utils.generate_template import get_markup

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def require_login():
    if 'user_id' not in session or session['user_id'] != 1:
        flash(
            get_markup(
                show_message='permission Denied'
            ), 'danger'
        )
        return redirect(url_for('main.index'))


@admin_bp.route("/", methods=['GET'])
def index():
    user_id = session['user_id']
    user_name = session['username']

    users = UserHandler.get_all()

    channels, ok = ChannelsHandler.get_all_channels()

    return render_template(
        "admin.html",
        user_name=user_name,
        users=users,
        channels=channels
    )
