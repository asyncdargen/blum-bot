from random import randint
from time import sleep


class IntRange:

    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def random(self):
        return randint(self.start, self.stop)

    def sleep_random(self):
        sleep(self.random())


def range(start: int, stop: int) -> IntRange:
    return IntRange(start, stop)
