from flask import current_app

from app.hyldb.models.messgaes import Messages, MessageState


class MessagesHandler:

    @staticmethod
    def get_messgae(message_id: int):
        return Messages.get_one_by_id(oid=message_id)

    @staticmethod
    def add_message(user_id: int, channel_id: int, content: str, state: MessageState = MessageState.NORMAL):
        ok = True
        try:
            res = Messages.add(user_id=user_id, channel_id=channel_id, content=content, state=state)
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
