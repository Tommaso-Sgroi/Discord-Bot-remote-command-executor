import datetime

from drce.reader.reader import Reader


class CommandConsoleReader(Reader):
    def read(self) -> str:
        return input(f'[{datetime.datetime.now()}]>>> ').strip()
