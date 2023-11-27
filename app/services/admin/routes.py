from flask import Blueprint, session, request, render_template, redirect, url_for, current_app, flash, jsonify

from app.utils.generate_template import get_markup

from app.extensions import message_filter
from app.hyldb.handler.users import UserHandler
from app.hyldb.handler.channels import ChannelsHandler
from app.hyldb.handler.banwords import BanWordsHandler


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

    banned_words = BanWordsHandler.get_all()

    active_label = request.args.get('active_label')
    return render_template(
        "admin.html",
        user_name=user_name,
        users=users,
        channels=channels,
        banned_words=banned_words,
        active_label=active_label
    )

@admin_bp.route("/banwords/add", methods=['POST'])
def add_banwords():
    banword = request.form.get('added_word').lower()
    # current_app.logger.info(f"Recv: {banword}")
    if BanWordsHandler.add(banword):
        message_filter.add(banword)
        flash(
            get_markup(
                show_message="Add success"
            ), 'success'
        )
    else:
        flash(
            get_markup(
                show_message="Add error, please try later"
            ), 'danger'
        )

    return redirect(url_for('admin.index', active_label=3))

@admin_bp.route("/banwords/remove", methods=['POST'])
def remove_banwords():
    word = request.form.get('word')
    if BanWordsHandler.remove(word):
        message_filter.remove(word)
        flash(
            get_markup(
                show_message="Delete success"
            ), 'success'
        )
    else:
        flash(
            get_markup(
                show_message="Delete error, please try later"
            ), 'danger'
        )

    return redirect(url_for('admin.index', active_label=3))
