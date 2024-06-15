from util.range import range
from client.data import ClientData

clients = [
    ClientData("dinya", None),
    ClientData("eva", None),
    ClientData("arbuz", None)
]  # Clients with first refresh_token (u can specify it in sessions/{client_name}.session in first line)

actions = {
    "farming": True,
    "game": False,
    "daily": True,
    "tasks": True,
    "friends": True
}

game_delay = range(50, 70)  # time run delay (in seconds)
game_points = range(250, 280)  # points to get in game

work_delay = range(30, 70)  # delay between actions (in seconds)
work_dummy_delay = range(5, 10)  # delay if no work (is seconds)

fetch_delay = range(15, 30)  # delay between fetches (used for dumping, is seconds)
fetch_split_delay = range(2, 5)  # delay between clients pair fetches

dump_bot_token = None  # work token or None for no dumping
dump_profile_id = 1497967816 # profile id (who will receive dump message)
dump_delay = 5  # delay between dump data in telegram (is seconds)
