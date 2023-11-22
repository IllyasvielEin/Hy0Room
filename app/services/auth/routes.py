from flask import Blueprint, session, request, redirect, url_for, flash, current_app, render_template

from app.utils.generate_template import get_markup
from app.hyldb.handler.users import UserHandler

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
        res, ok = UserHandler.get_user_by_name(username)
        if not ok:
            return "Internal error", 500
        if res is None:
            flash(
                get_markup(
                    iclass="fa fa-2x fa-info-circle",
                    show_message=f" User {username} not found"
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

    real_name = request.form.get('real_name')
    student_id = request.form.get('student_id')

    res, ok = UserHandler.add_user(username=username, password=password, student_id=student_id, real_name=real_name)
    if ok:
        flash(
            get_markup(
                iclass="fa fa-2x fa-info-circle",
                show_message=f"New username {username} created"
            ), 'info'
        )
        session['username'] = username
        session['user_id'] = res.id
    else:
        flash(
            get_markup(
                show_message="Internal error"
            ), 'danger'
        )
    return redirect(url_for('channels.get_channels'))


@auth_bp.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
        flash(
            get_markup(
                iclass="fa fa-2x fa-check-square-o",
                show_message=f"Logged out"
            )
        )
    return redirect(url_for('main.index'))
