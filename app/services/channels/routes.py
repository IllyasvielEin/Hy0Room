import json

from flask import Blueprint, request, session, redirect, url_for, current_app, flash, render_template

from app.hyldb.handler.channels import ChannelsHandler
from app.hyldb.handler.users import UserHandler
from app.hyldb.handler.messages import MessageState
from app.utils.generate_template import get_markup

channels_bp = Blueprint('channels', __name__, url_prefix="/channels")


@channels_bp.before_request
def require_login():
    if 'user_id' not in session:
        flash(
            get_markup(
                show_message="Please Login"
            ), 'danger'
        )
        return redirect(url_for('main.index'))

@channels_bp.route("/", methods=['GET'])
def get_channels():
    user_id = session.get('user_id')
    username = session.get('username')
    if username is None:
        return redirect(url_for('main.index'))

    user, ok = UserHandler.get_user_by_id(user_id=user_id)
    if not ok:
        flash(
            get_markup(
                show_message="Internal error"
            ),
            'warning'
        )
        current_app.logger.error("User find error")
        return redirect(url_for('channels.get_channels'))
    else:
        if user is None:
            session.clear()
            return redirect(url_for("main.index"))
        else:
            # channels = UserHandler.get_channels_info(username)
            channels, ok = ChannelsHandler.get_all_channels(brief=True)
            if not ok:
                return "Internal Error", 500
            # current_app.logger.info(f"Get channels: {channels}")
            last_visit = session.get('last_visit')

            return render_template(
                "channels.html",
                user_id=user_id,
                username=username,
                channels=channels,
                last_visit=last_visit
            )


@channels_bp.route("/<int:channel_id>", methods=['GET'])
def get_channel(channel_id):
    # set_last_channel
    user_id = session.get('user_id')
    username = session.get('username')
    session['last_visit'] = channel_id
    chats = ChannelsHandler.get_chats(channel_id)
    chats_dict = [x.to_dict() for x in chats if x.state == MessageState.NORMAL]

    # current_app.logger.info(f"Chats: {chats_dict}")

    return render_template(
        "channel.html",
        user_id=user_id,
        username=username,
        channel=channel_id,
        chats=chats_dict
    )


@channels_bp.route("/add", methods=['POST'])
def add_channel():
    markup_content = None
    category = None
    return_content = "channels.get_channels"

    new_channel = request.form.get('new_channel').strip()
    if new_channel != "":
        res, ok = ChannelsHandler.find_channel(new_channel)
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
                ok = ChannelsHandler.create_channel(new_channel)
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
