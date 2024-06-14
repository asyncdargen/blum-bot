from client.data import ClientData
from client.auth import BlumAuth

from time import time
from requests import *

BLUM_ENDPOINT = 'https://game-domain.blum.codes/api/v1'


class BlumClient:
    last_fetch: bool
    balance: float
    passes: int
    farming_end: int

    def __init__(self, data: ClientData):
        self.data = data
        self.auth = BlumAuth(data)

    def log(self, text):
        print(f'{self.data.name}: {text}')

    def fetch(self, retry: bool = False) -> bool:
        response = self.__request_get('/user/balance')

        if response.status_code != 200:
            self.last_fetch = False
            return False

        try:
            json = response.json()

            self.last_fetch = True

            self.balance = float(json['availableBalance'])
            self.passes = int(json['playPasses'])

            self.farming_end = 0
            self.farming_end = json['farming']['endTime']
        except Exception as e:
            print(e)
            return False

        return True

    def claim_daily(self):
        response = self.__request_post('/daily-reward?offset=-180')

        if response.status_code != 200:
            return False

        return True

    def fetch_available_tasks(self):
        response = self.__request_get('/tasks')

        if response.status_code != 200:
            return None

        try:
            json = response.json()
            tasks = {}

            def fetch_task(task):
                if task['type'] in ['SOCIAL_SUBSCRIPTION', 'APPLICATION_LAUNCH'] and task['status'] not in ['FINISHED', 'STARTED']:
                    tasks[task['id']] = task['status'] == 'READY_FOR_CLAIM'
                    return True

                return False

            for task in json:
                match task['type']:
                    case 'SOCIAL_SUBSCRIPTION':
                        fetch_task(task)
                    case 'PARTNER_INTEGRATION':
                        sub_tasks = task['subTasks']
                        completed = True

                        for sub_task in sub_tasks:
                            if sub_task['status'] != 'FINISHED':
                                completed = False
                                fetch_task(sub_task)

                        if completed:
                            tasks[task['id']] = True

            return tasks
        except Exception as e:
            print(e)

        return None

    def start_task(self, task_id):
        response = self.__request_post(f'/tasks/{task_id}/start')

        if response.status_code != 200:
            return False

        return True

    def claim_task(self, task_id):
        response = self.__request_post(f'/tasks/{task_id}/claim')

        if response.status_code != 200:
            return False

        return True

    def run_farming(self):
        response = self.__request_post('/farming/start')

        if response.status_code != 200:
            return False

        return True

    def claim_farming(self) -> bool:
        response = self.__request_post('/farming/claim')

        if response.status_code != 200:
            return False

        return True

    def play_game(self) -> str | None:
        response = self.__request_post('/game/play')

        if response.status_code != 200:
            return None

        try:
            json = response.json()

            return json['gameId']
        except Exception as e:
            print(e)
            return None

    def claim_game(self, game_id: str, points: int) -> True:
        response = self.__request_post('/game/claim', {
            'gameId': game_id,
            'points': points
        })

        if response.status_code != 200:
            return False

        self.balance += points

        return True

    def is_farming_run(self):
        return self.farming_end != 0

    def farming_remaining(self):
        return 0 if not self.is_farming_run() else self.farming_end - time() * 1000

    def is_farming_end(self):
        return self.farming_end < time() * 1000

    def __request_get(self, path: str, retry: bool = False) -> Response:
        response = get(f'{BLUM_ENDPOINT}{path}', headers=self.__prepare_headers())

        if response.status_code == 401 and not retry:
            self.auth.auth()
            return self.__request_get(path, True)

        return response

    def __request_post(self, path: str, body: dict | None = None, retry: bool = False) -> Response:
        response = post(f'{BLUM_ENDPOINT}{path}', json=body, headers=self.__prepare_headers())

        if response.status_code == 401 and not retry:
            self.auth.auth()
            return self.__request_post(path, body, True)

        return response

    def __prepare_headers(self) -> dict:
        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Authorization': f'Bearer {self.auth.token}',
            'Origin': 'https://telegram.blum.codes',
            'Priority': 'u=1, i',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'some-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
