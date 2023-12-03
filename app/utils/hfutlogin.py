import yaml
import time
import base64
import requests
from enum import Enum
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class AuthErrorType(Enum):
    NETWORKERROR = 1
    AUTHERROR = 2


class SchoolLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.cookies.clear()
        print(f"User {self.username} identified by {self.password}")

    def check(self):
        response = self.get_cookies()
        if response.status_code != 200:
            print("Network error")
            exit(0)
        encryption_pwd = self.encryption_pwd(self.password)
        if encryption_pwd == '':
            print("Encrypt error")
            exit(0)
        # print(encryption_pwd)
        # response = self.authen(student_id=self.username, pwd=encryption_pwd)
        response = self.get_TGC(encryption_pwd)
        return response.status_code == 200

    def get_secret(self):
        url = "https://cas.hfut.edu.cn/cas/oauth2.0/authorize?response_type=code&client_id=BsHfutEduPortal&redirect_uri=https://one.hfut.edu.cn/home/index"
        # params = {
        #     'response_type': 'code',
        #     'client_id': 'BsHfutEduPortal',
        #     'redirect_uri': 'https://one.hfut.edu.cn/home/index'
        # }
        response = self.session.get(url)
        return response

    def get_TGC(self, password):
        url = "https://cas.hfut.edu.cn/cas/login"

        params = {
            'service': 'https://cas.hfut.edu.cn/cas/oauth2.0/callbackAuthorize?client_id=BsHfutEduPortal&redirect_uri=https%3A%2F%2Fone.hfut.edu.cn%2Fhome%2Findex&response_type=code&client_name=CasOAuthClient'
        }

        data = {
            'username': self.username,
            'capcha': '',
            'execution': 'e1s1',
            '_eventId': 'submit',
            'password': password,
            'geolocation': ""
        }

        response = self.session.post(url, params=params, data=data, allow_redirects=False)
        return response

    def encryption_pwd(self, pwd):
        flavoring = self.session.cookies.get('LOGIN_FLAVORING')
        if flavoring is None:
            return ''
        key = flavoring.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        pwd_padded = pad(pwd.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(pwd_padded)
        encrypted_b64 = base64.b64encode(encrypted)
        return encrypted_b64

    def get_timestamp(self):
        res = int(time.time() * 1000)
        # print(res)
        return res

    def authen(self, student_id, pwd):
        url = 'https://cas.hfut.edu.cn/cas/policy/checkUserIdenty'
        timestamp = self.get_timestamp()
        params = {
            'username': student_id,
            'password': pwd,
            '_': f'{timestamp}'
        }
        response = self.session.get(url, params=params)

        return response

    def get_cookies(self):
        url = 'https://cas.hfut.edu.cn/cas/checkInitParams'
        params = {
            '_': f'{self.get_timestamp()}'
        }
        self.session.get(url, params=params)
        url = 'https://cas.hfut.edu.cn/cas/login'
        response = self.session.get(url)

        return response


if __name__ == "__main__":
    with open("../../abc.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    username = cfg['username']
    password = cfg['password']

    loginer = SchoolLogin(username, password)
    if loginer.check():
        print("Login ok")
    else:
        print("Login error")
