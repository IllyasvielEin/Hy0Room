from flask import Blueprint, session, request, render_template, redirect, url_for, current_app, flash, jsonify
from flask_login import current_user, logout_user, login_user

from app.hyldb.handler.users import UserHandler, Users
from app.utils.generate_template import get_markup

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.before_request
def require_login():
    if not current_user.is_authenticated:
        # flash(
        #     get_markup(
        #         show_message="Please Login"
        #     ), 'danger'
        # )
        # current_app.logger.info("Unauthenticated")
        return redirect(url_for('main.index'))

@user_bp.route('/<int:user_id>')
def profile(user_id: int):
    if user_id == 1 and current_user.get_id() == 1:
        return redirect(url_for('admin.index'))

    res, ok = UserHandler.get_user_by_id(user_id)
    if not ok or res is None:
        flash(
            get_markup(
                show_message="Empty user"
            ), 'danger'
        )
        return redirect(url_for('user.profile', user_id=user_id))

    user_info = {
        'username': res.username,
        'real_name': res.details.real_name,
        'student_id': res.details.student_id
    }

    return render_template(
        "user.html",
        view_user_id=user_id,
        user_info=user_info
    )


@user_bp.route('/<int:user_id>/update', methods=['POST'])
def update(user_id: int):

    request_user_id = current_user.get_id()
    if int(request_user_id) != user_id:
        return jsonify({'status': 'not matching user_id'}), 400

    ok = True
    try:
        form = request.form.to_dict()
        filtered_form = {k: v for k, v in form.items()
                         if (v is not None and
                             str(v).strip() not in [''] and
                             k in ['username', 'password']
                             )
                         }
        res, ok = UserHandler.update_user_info(user_id=user_id, kv=filtered_form)
        # current_app.logger.info(f"form: {form}")
        if ok:
            logout_user()
            login_user(res)
    except Exception as e:
        current_app.logger.error(f'{e}')
        ok = False
    if ok:
        flash(
            get_markup(
                show_message="Update ok"
            ), 'success'
        )
    else:
        flash(
            get_markup(
                show_message="Update failed"
            ), 'danger'
        )

    return redirect(url_for('user.profile', user_id=user_id))