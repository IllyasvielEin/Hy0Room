import re
from typing import List


class MessageFilter:
    def __init__(self):
        self._ban_words_list = set()

    def add(self, word: str | List[str]):
        if isinstance(word, list):
            self._ban_words_list.update(word)
        elif isinstance(word, str):
            self._ban_words_list.add(word)

    def remove(self, word):
        self._ban_words_list.remove(word)

    def get_words(self):
        return self._ban_words_list

    def mes_filter(self, mes, custom_func=lambda match: '*' * len(match.group(0))):
        if len(self._ban_words_list) == 0:
            return mes

        pattern = '|'.join(map(re.escape, self._ban_words_list))  # 构建匹配的正则表达式模式
        if isinstance(mes, str):
            res = re.sub(pattern, custom_func, mes)
        elif isinstance(mes, list):
            res = []
            for each_mes in mes:
                res.append(re.sub(pattern, custom_func, each_mes))
        else:
            res = mes
        return res
