from flask import Blueprint, session, request, redirect, url_for, flash, current_app, render_template
from markupsafe import Markup

from app.hyldb.handler.user import UserHandler

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        username = session.get('username')
        channels = UserHandler.get_channels_info(username)
        last_visit = session.get('last_visit')
        return render_template(
            "channels.html",
            username=username,
            channels=channels,
            last_visit=last_visit
        )
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        current_app.logger.info(f"{username} login identified by {password}")
        if username is None or password is None:
            return 'error input', 400
        res, ok = UserHandler.find_user(username)
        if not ok:
            return "Internal error", 500
        if res is None:
            flash(
                Markup(
                    """<i class='fa fa-2x fa-info-circle'></i>
                        User %s not found.""" % username
                ), 'info'
            )
        else:
            session['username'] = username
            session['user_id'] = res.id
        return redirect(url_for("channels.get_channels"))


@auth_bp.route("/register", methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    current_app.logger.info(f"{username} register by {password}")
    res, ok = UserHandler.add_user(username=username, password=password)
    if ok:
        flash(
            Markup(
                """<i class='fa fa-2x fa-info-circle'></i>
                New username %s created.""" % username
            ), 'info'
        )
        session['username'] = username
        session['user_id'] = res.id
    return redirect(url_for('channels.get_channels'))


@auth_bp.route('/logout')
def logout():
    if 'token' in session:
        session.clear()
        flash(
            Markup(
                """<i class='fa fa-2x fa-check-square-o'></i>
                You have logged out."""
            ), 'success'
        )
    return redirect(url_for('main.index'))
