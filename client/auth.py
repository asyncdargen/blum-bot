from client.data import ClientData
from requests import *


class BlumAuth:

    def __init__(self, data: ClientData):
        self.data = data

        self.token = None
        self.refresh_token = None

        self.__load_token()

    def auth(self) -> bool:
        response = post('https://gateway.blum.codes/v1/auth/refresh', json={'refresh': self.refresh_token})

        if response.status_code != 200:
            return False

        try:
            json = response.json()
            self.token = json['access']
            self.refresh_token = json['refresh']

            self.__store_token()
        except Exception as e:
            print(e)
            return False

        return True

    def __store_token(self):
        with open(f'sessions/{self.data.name}.session', 'w') as session:
            session.write(self.refresh_token)
            session.write('\n')
            session.write(self.token)

    def __load_token(self):
        self.refresh_token = self.data.refresh_token
        try:
            with open(f'sessions/{self.data.name}.session', 'r') as session:
                self.refresh_token = session.readline().replace('\n', '')
                self.token = session.readline().replace('\n', '')
        except:
            pass