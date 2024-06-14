from work.bot import run_fetch, run_work, clients
from work.dumper import run_dump

print('Staring BlumBot')
print(f'Loaded {len(clients)} accounts')

run_fetch()
run_dump()
run_work()
