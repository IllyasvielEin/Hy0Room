from flask import Blueprint, request, render_template, redirect, url_for, current_app, flash, jsonify
from flask_login import current_user

from app.hyldb.handler.messages import MessagesHandler
from app.hyldb.handler.permission import PermissionHandler
from app.hyldb.handler.posts import PostsHandler
from app.hyldb.handler.reports import ReportsHandler, ReportType
from app.hyldb.models.messgaes import MessageState
from app.utils.generate_template import get_markup

from app.extensions import message_filter
from app.hyldb.handler.users import UserHandler, UserType
from app.hyldb.handler.channels import ChannelsHandler
from app.hyldb.handler.banwords import BanWordsHandler

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def require_login():
    if not current_user.is_authenticated or current_user.get_id() != 1:
        flash(
            get_markup(
                show_message='permission Denied'
            ), 'danger'
        )
        return redirect(url_for('main.index'))


@admin_bp.route("/", methods=['GET'])
def index():
    user_id = current_user.get_id()
    user_name = current_user.get_username()

    users = UserHandler.get_all()

    channels, ok = ChannelsHandler.get_all_channels()

    banned_words = BanWordsHandler.get_all()

    new_users = UserHandler.get_all_new()

    reports = ReportsHandler.get_all_needed_judge()

    active_label = request.args.get('active_label')
    return render_template(
        "admin.html",
        user_name=user_name,
        users=users,
        channels=channels,
        banned_words=banned_words,
        active_label=active_label,
        new_users=new_users,
        reported_entries=reports
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


@admin_bp.route('/user/<int:user_id>/approve')
def approve_new_user(user_id: int):
    res, ok = UserHandler.update_user_info(
        user_id=user_id,
        kv={
            'state': UserType.NORMAL
        }
    )
    if ok:
        show_message = 'Approve ok'
        category = 'success'
    else:
        show_message = 'Approve error'
        category = 'danger'
    flash(
        get_markup(
            show_message=show_message
        ), category
    )
    return redirect(url_for('admin.index', active_label=4))


@admin_bp.route('/user/<int:user_id>/reject')
def reject_new_user(user_id: int):
    res, ok = UserHandler.update_user_info(
        user_id=user_id,
        kv={
            'state': UserType.REGISTER_REJECTED
        }
    )
    if ok:
        show_message = 'Reject ok'
        category = 'success'
    else:
        show_message = 'Reject error'
        category = 'danger'
    flash(
        get_markup(
            show_message=show_message
        ), category
    )
    return redirect(url_for('admin.index', active_label=4))


@admin_bp.route('/ban_user/<int:user_id>', methods=['GET'])
def ban_user(user_id):
    show_messages = 'Ban ok'
    category = 'success'

    this_user_id = current_user.get_id()
    if not PermissionHandler.a_is_higher_permission(this_user_id, user_id):
        show_messages = 'Permission deny'
        category = 'danger'

    res, ok = UserHandler.update_user_info(
        user_id,
        kv={
            'state': UserType.BANNED
            # 'state_descript':
        }
    )
    if not ok:
        show_messages = 'Ban error'
        category = 'danger'

    flash(
        get_markup(
            show_message=show_messages
        ), category
    )

    return redirect(url_for('admin.index', activbe_label=5))

@admin_bp.route('/report/<int:report_id>', methods=['GET'])
def judge_this(report_id: int):
    show_messages = 'Judge ok'
    category = 'success'

    this_user_id = current_user.get_id()
    guilty: bool = request.args.get('guilty').lower() == 'true'
    ok = ReportsHandler.find_guilty(report_id=report_id, guilty=guilty)

    if ok:
        report = ReportsHandler.get_one(report_id)
        content_id = report.content_id
        if guilty:
            if report.content_type == ReportType.CHANNEL_CHAT:
                MessagesHandler.set_state(content_id, MessageState.VIOLATION)
            elif report.content_type == ReportType.POST:
                PostsHandler.judge_post(post_id=content_id, guilty=True)
        else:
            if report.content_type == ReportType.CHANNEL_CHAT:
                MessagesHandler.set_state(content_id, MessageState.NORMAL)
            elif report.content_type == ReportType.POST:
                PostsHandler.judge_post(post_id=content_id, guilty=False)

    else:
        show_messages = 'Judge error'
        category = 'danger'

    flash(
        get_markup(
            show_message=show_messages
        ), category
    )

    return redirect(url_for('admin.index', activbe_label=5))
