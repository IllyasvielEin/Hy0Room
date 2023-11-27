from flask import current_app
from app.hyldb.models.banwords import BanWords


class BanWordsHandler:
    @staticmethod
    def get_all():
        try:
            res = BanWords.get()
        except Exception as e:
            current_app.logger.error(f"{e}")
            res = None
        return res

    @staticmethod
    def add(word: str):
        try:
            res = BanWords.add(
                word=word
            )
        except Exception as e:
            current_app.logger.error(f"{e}")
            return False
        return True

    @staticmethod
    def remove(word: int | str):
        try:
            if isinstance(word, int):
                BanWords.delete(oid=word)
            else:
                BanWords.delete(filters={'word': word})
        except Exception as e:
            current_app.logger.error(f'{e}')
            return False
        return True
