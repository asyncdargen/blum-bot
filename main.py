from time import sleep

from work.bot import run_fetch, run_work, clients
from work.dumper import run_dump

run_fetch()
run_dump()
run_work()
