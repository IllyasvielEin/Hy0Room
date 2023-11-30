import yaml
import hashlib

import requests
from enum import Enum

class AuthErrorType(Enum):
    NETWORKERROR = 1
    AUTHERROR = 2

class HFUTLogin:
    def check(self, username, password):
        response = self.get_salt()
        if response.status_code != 200:
            return AuthErrorType.NETWORKERROR
        salt = response.content.decode()
        cookies = response.headers.get('Set-Cookie')
        response = self.auth_login(
            username=username, password=password, salt=salt, cookies=cookies
        )
        # print(response.content.decode())
        # print(response.status_code)

    def get_salt(self):
        data = {}
        cookies = {'SRVID': 's114'}
        url = 'http://jxglstu.hfut.edu.cn/eams5-student/login-salt'

        response = requests.get(url, data=data, cookies=cookies)
        return response

    def auth_login(self, username, password, salt, cookies: str):
        url = 'http://jxglstu.hfut.edu.cn/eams5-student/login'
        hashed_password = hashlib.sha1((salt + '-' + password).encode()).hexdigest()
        cookies = {'SRVID': f's114; {cookies}'}
        print(cookies)
        data = {
            'username': username,
            'password': hashed_password,
            'captcha': '',
        }
        # response = requests.post(url, data=data, cookies=cookies)
        return


if __name__ == "__main__":
    with open("abc.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    username = cfg['username']
    password = cfg['password']

    loginer = HFUTLogin()
    loginer.check(username=username, password=password)
