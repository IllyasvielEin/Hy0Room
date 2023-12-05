import urllib.parse

from flask import Blueprint, current_app
from flask_socketio import join_room, leave_room, emit

from app.extensions import socketio, message_filter
from app.hyldb.handler.messages import MessagesHandler, MessageState

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    current_app.logger.info(f'join {room}')
    emit('status', {
        'msg': 'Connected',
        'room': room
    }, room=room
     )

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': 'Disconnected', 'room': room}, room=room)


@socketio.on("send msg")
def emit_msg(data):
    content = urllib.parse.unquote(data['content'])
    # current_app.logger.info(f"emit: {content}")
    if content != '':
        fcontent = message_filter.mes_filter(mes=content.lower())
        content_state = MessageState.NORMAL
        if fcontent != content:
            content_state = MessageState.VIOLATION
        user_id = urllib.parse.unquote(data['user_id'])
        channel_id = urllib.parse.unquote(data['channel_id'])
        res, ok = MessagesHandler.add_message(user_id=int(user_id), channel_id=int(channel_id), content=content, state=content_state)
        if ok:
            emit(
                'emit msg',
                {
                    'mes_id': res.id,
                    'user_id': user_id,
                    'username': urllib.parse.unquote(data['username']),
                    'send_at': data['send_at'],
                    'content': fcontent,
                    'channel_id': channel_id
                }, room=channel_id
            )
        else:
            current_app.logger.error(f"mes insert error")

@socketio.on("del msg")
def del_msg(data):
    channel_id = data['channel']
    mes_data_id = data['id']
    # current_app.logger.info(f"{mes_data_id} delete")
    MessagesHandler.set_state(mes_id=mes_data_id, state=MessageState.WITHDRAWN)
    emit(
        'recall msg',
        {
            'channel_id': channel_id,
            'mes_data_id': mes_data_id
        },
        room=channel_id
    )

