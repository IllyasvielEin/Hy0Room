import json

from flask import Blueprint, request, redirect, url_for, session, current_app, flash, render_template
from flask_login import current_user

from app.hyldb.handler.channels import ChannelsHandler
from app.hyldb.handler.posts import PostsHandler
from app.hyldb.handler.reports import ReportsHandler
from app.hyldb.handler.users import UserHandler
from app.hyldb.handler.messages import MessageState, MessagesHandler
from app.hyldb.models.reports import ReportType
from app.utils.generate_template import get_markup

from app.extensions import message_filter, user_manager

channels_bp = Blueprint('channels', __name__, url_prefix="/channels")


@channels_bp.before_request
def require_login():
    if not current_user.is_authenticated:
        flash(
            get_markup(
                show_message="Please Login"
            ), 'danger'
        )
        return redirect(url_for('main.index'))


@channels_bp.route("/<int:channel_id>", methods=['GET'])
def get_channel(channel_id):
    user_id = current_user.get_id()
    username = current_user.get_username()

    if not user_manager.add_user(channel_id=channel_id, user=user_id):
        flash(
            get_markup(
                show_message="频道人满为患!"
            ), 'danger'
        )
        return redirect(url_for('main.index'))

    channel = ChannelsHandler.get_channel_by_id(channel_id)

    if channel is None:
        flash(
            get_markup(
                show_message="Empty channel"
            ), 'danger'
        )
        return redirect(url_for('main.index'))

    # set_last_channel
    session['last_visit_channel_id'] = channel_id
    session['last_visit_channel_name'] = channel.name

    chats = channel.messages
    chats_dict = [x.to_dict() for x in chats if x.state == MessageState.NORMAL]
    # for chat in chats_dict:
    #     chat['content'] = message_filter.mes_filter(chat)

    # current_app.logger.info(f"Chats: {chats_dict}")

    channel_users_id = user_manager.get_channel_user(channel_id=channel_id)
    current_app.logger.info(f"{user_manager.get_channel_user(channel_id)}")
    channel_users = UserHandler.get_all_id_in_list(channel_users_id)

    return render_template(
        "channel.html",
        user_id=user_id,
        username=username,
        channel_id=channel_id,
        channel_name=channel.name,
        chats=chats_dict,
        chanel_users=channel_users
    )


@channels_bp.route("/add", methods=['POST'])
def add_channel():
    markup_content = None
    category = None
    return_content = "main.index"

    request_user_id = current_user.get_id()
    new_channel = request.form.get('new_channel').strip()
    channel_description = request.form.get('channel_description').strip()

    if new_channel != "":
        res, ok = ChannelsHandler.get_channel_by_name(new_channel)
        if not ok:
            markup_content = get_markup(
                iclass="fa fa-2x fa-warning",
                show_message=f"Add channel {new_channel} error, please try again later."
            )
            category = 'warning'
        else:
            if res is not None:
                markup_content = get_markup(
                    iclass='fa fa-2x fa-warning',
                    show_message=f"Channel {new_channel} already exists."
                )
                category = 'warning'
            else:
                ok = ChannelsHandler.create_channel(
                    creator_id=request_user_id,
                    channel_name=new_channel,
                    channel_description=channel_description
                )
                if ok:
                    markup_content = get_markup(
                        iclass='fa fa-2x fa-check-square-o',
                        show_message=f"Error occur new channel {new_channel} create."
                    )
                    category = 'success'
                else:
                    markup_content = get_markup(
                        iclass='fa fa-2x fa-warning',
                        show_message=f"Add channel {new_channel} error, please try again later."
                    )
                    category = 'warning'

    if markup_content is not None:
        flash(markup_content, category=category)

    return redirect(url_for(return_content))


@channels_bp.route('/<int:channel_id>/report/<int:message_id>', methods=['GET'])
def report_message(channel_id, message_id):
    show_message = 'Report ok'
    category = 'success'
    message = MessagesHandler.get_messgae(message_id)
    channel = ChannelsHandler.get_channel_by_id(channel_id=channel_id)
    if message is not None:
        res = ReportsHandler.add_reports(
            content_id=message_id,
            content=message.content,
            content_type=ReportType.CHANNEL_CHAT,
            accuser_id=int(current_user.get_id()),
            accused_id=message.user.id
        )
        if res is None:
            show_message = 'Report error'
            category = 'danger'
    else:
        show_message = f'Report message[{message_id}] is not found'
        category = 'danger'

    flash(
        get_markup(
            show_message=show_message
        ), category
    )

    return redirect(url_for('channels.get_channel', channel_id=channel_id))
