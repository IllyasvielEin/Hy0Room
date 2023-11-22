from flask import current_app

from app.hyldb.models.messgaes import Messages, MessageState


class MessagesHandler:

    @staticmethod
    def add_message(user_id, channel_id, content):
        ok = True
        try:
            res = Messages.add(user_id=user_id, channel_id=channel_id, content=content)
        except Exception as e:
            current_app.logger.error(f"{e}")
            ok = False
            res = None
        return res, ok

    @staticmethod
    def del_message(message_id):
        ok = Messages.delete(oid=message_id)
        return ok

    @staticmethod
    def set_state(mes_id: int, state: MessageState):
        Messages.update(oid=mes_id, kv={"state": state})
