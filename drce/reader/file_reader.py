from .reader import Reader


class CommandScriptFileReader(Reader):
    def __init__(self, script_path: str):
        super().__init__()
        self.commands = []
        with open(script_path, mode="r", encoding="utf-8") as f:
            self.commands = f.read().splitlines()

        self._internal_command_iterator = iter(self)

    def __iter__(self):
        return iter(self.commands)

    def read(self) -> str:
        return next(self._internal_command_iterator).strip()
