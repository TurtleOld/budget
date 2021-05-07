import os
import requests
import random
from dotenv import load_dotenv


def result_receipt():
    client = NalogRuPython()
    qr_code = "t=20200725T140000&s=1398.00&fn=9282000100386709&i=43134&fp=2379617251&n=1"
    ticket = client.get_ticket(qr_code)
    return ticket


# chars = "ABCDEF1234567890"
# for n in range(1):
#     result_random = ""
#     for i in range(30):
#         result_random += random.choice(chars)
#         print(result_random)


class NalogRuPython:
    HOST = 'irkkt-mobile.nalog.ru:8888'
    DEVICE_OS = 'Android'
    CLIENT_VERSION = '2.9.0'
    DEVICE_ID = '974A34887DBA6A1B'
    ACCEPT = '*/*'
    USER_AGENT = 'billchecker/2.9.0 (iPhone; iOS 13.6; Scale/2.00)'
    ACCEPT_LANGUAGE = 'ru-RU;q=1, en-US;q=0.9'

    def __init__(self):
        load_dotenv()  # read environments from .env file
        self.__session_id = None
        self.set_session_id()

    def set_session_id(self) -> None:
        """
        Authorization using INN and password of user lk nalog.ru
        """
        if os.getenv('CLIENT_SECRET') is None:
            raise ValueError('OS environments not content "CLIENT_SECRET"')
        if os.getenv('INN') is None:
            raise ValueError('OS environments not content "INN"')
        if os.getenv('PASSWORD_NALOG') is None:
            raise ValueError('OS environments not content "PASSWORD"')

        url = f'https://{self.HOST}/v2/mobile/users/lkfl/auth'
        payload = {
            'inn': os.getenv('INN'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'password': os.getenv('PASSWORD')
        }
        headers = {
            'Host': self.HOST,
            'Accept': self.ACCEPT,
            'Device-OS': self.DEVICE_OS,
            'Device-Id': self.DEVICE_ID,
            'clientVersion': self.CLIENT_VERSION,
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'User-Agent': self.USER_AGENT,
        }

        resp = requests.post(url, json=payload, headers=headers)
        self.__session_id = resp.json()['sessionId']

    def _get_ticket_id(self, qr: str) -> str:
        """
        Get ticker id by info from qr code
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: Ticket id. Example "5f3bc6b953d5cb4f4e43a06c"
        """
        url = f'https://{self.HOST}/v2/ticket'
        payload = {'qr': qr}
        headers = {
            'Host': self.HOST,
            'Accept': self.ACCEPT,
            'Device-OS': self.DEVICE_OS,
            'Device-Id': self.DEVICE_ID,
            'clientVersion': self.CLIENT_VERSION,
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'sessionId': self.__session_id,
            'User-Agent': self.USER_AGENT,
        }

        resp = requests.post(url, json=payload, headers=headers)

        return resp.json()["id"]

    def get_ticket(self, qr: str) -> dict:
        """
        Get JSON ticket
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: JSON ticket
        """
        ticket_id = self._get_ticket_id(qr)
        url = f'https://{self.HOST}/v2/tickets/{ticket_id}'
        headers = {
            'Host': self.HOST,
            'sessionId': self.__session_id,
            'Device-OS': self.DEVICE_OS,
            'clientVersion': self.CLIENT_VERSION,
            'Device-Id': self.DEVICE_ID,
            'Accept': self.ACCEPT,
            'User-Agent': self.USER_AGENT,
            'Accept-Language': self.ACCEPT_LANGUAGE,
        }

        resp = requests.get(url, headers=headers)

        return resp.json()

