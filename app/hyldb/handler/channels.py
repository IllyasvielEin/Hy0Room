from flask import current_app
from app.hyldb.models.channels import Channels


class ChannelsHandler:

    @staticmethod
    def get_channel_by_id(channel_id: int):
        res = Channels.get_one_by_id(oid=channel_id)
        return res

    @staticmethod
    def get_channel_by_name(channel_name: str):
        tmp_filter = {
            "name": channel_name
        }
        ok = True
        try:
            res = Channels.get(filters=tmp_filter, limitc=1)
        except Exception as e:
            current_app.logger.error(f"Failed in find channel: {e}")
            res = None
            ok = False
        return res, ok

    @staticmethod
    def create_channel(creator_id: int, channel_name: str, channel_description: str | None = None):
        ok = True
        try:
            Channels.add(name=channel_name, description=channel_description, creator_id=creator_id)
        except Exception as e:
            current_app.logger.error(f"Failed in add channel: {e}")
            ok = False
        return ok

    @staticmethod
    def get_chats(channel_id):
        channel = Channels.get_one_by_id(oid=channel_id)
        # current_app.logger.info(str(channel))
        return channel.messages

    @staticmethod
    def get_all_channels():
        ok = True
        try:
            channels = Channels.get()
        except Exception as e:
            current_app.logger.error(f"Failed in add channel: {e}")
            ok = False
            channels = None

        return channels, ok
