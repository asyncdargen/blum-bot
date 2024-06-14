from threading import Thread
from time import sleep

import config
from client.client import BlumClient

clients = {client.data.name: client for client in map(BlumClient, config.clients)}


def run_fetch():
    def __run_fetch():
        while True:
            for client in clients.values():
                try:
                    client.fetch()
                except:
                    pass
                config.fetch_split_delay.sleep_random()
            config.fetch_delay.sleep_random()

    Thread(target=__run_fetch, daemon=True).start()


def __work_tasks(client):
    tasks = client.fetch_available_tasks()

    if tasks is None:
        client.log('Failed to fetch available tasks')
        return True
    elif len(tasks) > 0:
        client.log(f'Fetched {len(tasks)} available tasks')

        for task_id in tasks:
            if not tasks[task_id]:
                if client.start_task(task_id):
                    client.log(f'Task {task_id} started')
                    tasks[task_id] = True
                    sleep(3)
                else:
                    client.log(f'Failed task {task_id} start')
                    sleep(3)

            if tasks[task_id]:
                if tasks[task_id]:
                    if client.claim_task(task_id):
                        client.log(f'Task {task_id} claimed')
                        sleep(3)
                    else:
                        client.log(f'Failed task {task_id} claim')
                        sleep(3)

        return True

    return False


def __work_daily(client):
    if client.claim_daily():
        client.log('Claimed daily')
        return True

    return False


def __work_game(client):
    if client.passes > 0:
        game = client.play_game()
        if not game:
            client.log(f'Failed to play game {game}')
        else:
            points = config.game_points.random()
            client.log(f'Playing game {game} with {points} points')
            config.game_delay.sleep_random()
            if client.claim_game(game, points):
                client.log(f'Claimed game {game} with {points} points')
            else:
                client.log(f'Failed to claim game {game}')

        return True

    return False


def __work_farming(client):
    if client.is_farming_end():
        if client.claim_farming():
            client.log('Claimed farming')
            sleep(1)
            if client.run_farming():
                client.log('Started farming')
            else:
                client.log('Failed farming start')
        else:
            client.log('Failed farming claim')

        return True
    elif not client.is_farming_run():
        if client.run_farming():
            client.log('Started farming')
        else:
            client.log('Failed farming start')

        return True

    return False


def __work(client):
    work = False

    if not client.fetch():
        client.log('Client fetch failed')
        return True

    if __work_farming(client):
        work = True
        sleep(1.5)

    if __work_daily(client):
        work = True
        sleep(1.6)

    if __work_game(client):
        work = True
    elif __work_tasks(client):
        work = True

    return work


def run_work():
    while True:
        for client in clients.values():
            try:
                if __work(client):
                    config.work_delay.sleep_random()
                else:
                    config.work_dummy_delay.sleep_random()
            except:
                config.work_delay.sleep_random()
