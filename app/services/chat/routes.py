import urllib.parse

from flask import Blueprint, session, request, render_template, redirect, url_for, current_app
from flask_socketio import emit

from app.extensions import socketio
from app.hyldb.handler.messages import MessagesHandler

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@socketio.on("send msg")
def emit_msg(data):
    current_app.logger.info(f"emit: {data}")
    content = urllib.parse.unquote(data['content'])
    if content != '':
        user_id = urllib.parse.unquote(data['user_id'])
        channel_id = urllib.parse.unquote(data['channel_id'])
        res, ok = MessagesHandler.add_message(user_id=user_id, channel_id=channel_id, content=content)
        if ok:
            emit(
                'emit msg',
                {
                    'mes_id': res.id,
                    'username': data['username'],
                    'send_at': data['send_at'],
                    'content': content,
                    'channel_id': channel_id
                }
            )
