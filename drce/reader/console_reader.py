import datetime

from .reader import Reader


class CommandConsoleReader(Reader):
    def read(self) -> str:
        return input(f'[{datetime.datetime.now()}]>>> ').strip()
