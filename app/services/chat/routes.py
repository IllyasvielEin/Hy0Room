import urllib.parse
from flask_socketio import emit

from flask import Blueprint, session, request, render_template, redirect, url_for, current_app

from app.extensions import socketio
from app.hyldb.handler.messages import MessagesHandler, MessageState

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@socketio.on("send msg")
def emit_msg(data):
    # current_app.logger.info(f"emit: {data}")
    content = urllib.parse.unquote(data['content'])
    if content != '':
        user_id = urllib.parse.unquote(data['user_id'])
        channel_id = urllib.parse.unquote(data['channel_id'])
        res, ok = MessagesHandler.add_message(user_id=user_id, channel_id=channel_id, content=content)
        if ok:
            socketio.emit(
                'emit msg',
                {
                    'mes_id': res.id,
                    'user_id': user_id,
                    'username': data['username'],
                    'send_at': data['send_at'],
                    'content': content,
                    'channel_id': channel_id
                }
            )

@socketio.on("del msg")
def del_msg(data):
    channel_id = data['channel']
    mes_data_id = data['id']
    # current_app.logger.info(f"{mes_data_id} delete")
    MessagesHandler.set_state(mes_id=mes_data_id, state=MessageState.WITHDRAWN)
    socketio.emit(
        'recall msg',
        {
            'channel_id': channel_id,
            'mes_data_id': mes_data_id
        }
    )
