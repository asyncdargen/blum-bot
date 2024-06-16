from threading import Thread
from time import sleep

from requests import post

import config
from work.bot import clients
from client.client import BlumClient
from util.format import format_time

__enabled = config.dump_bot_token is not None
__message = -1


def __dump_client(client: BlumClient) -> str:
    return f"""{client.data.name} {'🟢' if client.last_fetch else '🔴'}:
    Баланс: {client.balance}
    Билеты: {client.passes} ({(client.passes * config.game_points.start + client.passes * config.game_points.stop) / 2.0})
    Фарминг: {'еще ' + format_time(client.farming_remaining()) if not client.is_farming_end() and client.is_farming_run() else 'не идет (странно)'}
"""

def __dump(clients):
    global __message

    text = '\n'.join(map(__dump_client, clients))

    total_balance = sum(map(lambda client: client.balance, clients))
    total_passes = sum(map(lambda client: client.passes, clients))
    text += f"""
Суммарно:
    Баланс: {total_balance}
    Билеты: {total_passes} ({(total_passes * config.game_points.start + total_passes * config.game_points.stop) / 2.0})
    Возможный баланс: {(total_passes * config.game_points.start + total_passes * config.game_points.stop) / 2.0 + total_balance}
"""
    if __message != -1:
        post(f'https://api.telegram.org/bot{config.dump_bot_token}/editMessageText', json={
            'chat_id': config.dump_profile_id,
            'text': text,
            'message_id': __message,
        })
    else:
        response = post(f'https://api.telegram.org/bot{config.dump_bot_token}/sendMessage', json={
            'chat_id': config.dump_profile_id,
            'text': text,
        })
        json = response.json()
        __message = int(json['result']['message_id'])


def run_dump():
    if __enabled:
        def __run_dump():
            while True:
                try:
                    sleep(config.dump_delay)
                    __dump(clients.values())
                except:
                    pass

        Thread(target=__run_dump, daemon=True).start()
