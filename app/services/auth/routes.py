from flask import Blueprint, session, request, redirect, url_for, flash, current_app, render_template

from app.extensions import user_manager
from app.utils.generate_template import get_markup
from app.hyldb.handler.users import UserHandler
from app.hyldb.handler.channels import ChannelsHandler

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template(
            "channels.html",
            username=None
        )
    elif request.method == "POST":
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        current_app.logger.info(f"{username} login identified by {password}")
        if username is None or password is None:
            current_app.logger.error(f"{username} login identified by {password}")
            flash(
                get_markup(
                    show_message="Check input"
                )
            )
            return redirect(url_for('auth.login'))
        res, ok = UserHandler.get_user_by_name(username)
        if not ok:
            flash(
                get_markup(
                    show_message="Internal error"
                )
            )
            return redirect(url_for('auth.login'))
        if res is None:
            flash(
                get_markup(
                    iclass="fa fa-2x fa-info-circle",
                    show_message=f" User {username} not found"
                ), 'info'
            )
            return redirect(url_for('auth.login'))
        else:
            if password == str(res.password):
                session['username'] = username
                session['user_id'] = res.id
            else:
                flash(
                    get_markup(
                        show_message="Error password"
                    ), 'danger'
                )
                return redirect(url_for('auth.login'))
        return redirect(url_for("channels.get_channels"))


@auth_bp.route("/register", methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    current_app.logger.info(f"{username} register by {password}")

    real_name = request.form.get('real_name')
    student_id = request.form.get('student_id')

    is_internal_error = False

    res, ok = UserHandler.get_user_by_name(username=username)
    if not ok:
        is_internal_error = True
    else:
        if res is not None:
            flash(
                get_markup(
                    show_message=f"{username} has been registered"
                )
            ), 'danger'
            return redirect(url_for('auth.login'))
        else:
            res, ok = UserHandler.add_user(
                username=username, password=password, student_id=student_id, real_name=real_name)
            if not ok:
                is_internal_error = True
            else:
                flash(
                    get_markup(
                        iclass="fa fa-2x fa-info-circle",
                        show_message=f"New username {username} created"
                    ), 'info'
                )
                session['username'] = username
                session['user_id'] = res.id

    if is_internal_error:
        flash(
            get_markup(
                show_message="Internal error"
            ), 'danger'
        )
        return redirect(url_for('auth.login'))

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
        user_id = session.get('user_id')
        user_manager.remove_user(user_id)
    return redirect(url_for('auth.login'))
