import logging
import abc
from typing import Sequence

all_ = "all"
"""Keyword all"""


class Command(abc.ABC):
    """
    Represent a general command that can be executed
    """

    def __init__(self, client, guild: Sequence[str | int]):
        self.client = client
        self.string_log = str(self.__class__.__name__) + " "
        self.logger = None
        if all_ in guild:
            self.guild = list(client.guilds)
        else:
            self.guild = [self.client.get_guild(int(g)) for g in guild]

    def __str__(self):
        name = type(self).__name__
        guilds = 'guilds affected: ['
        for guild in self.guild:
            guilds += (guild.name + ': ' + str(guild.id)) + ', '
        return name + ": \n" + guilds[:-2] + ']'

    def __hash__(self):
        return hash(str(self))

    def get_user_from_id(self, user_id):
        """
        Get user from id, it works only if there is only one guild
        :param user_id: user id integer
        :return: Member object of the guild
        """
        for guild in self.guild:
            user = guild.get_member(user_id)
            if user is not None:
                return user

    @abc.abstractmethod
    async def run(self):
        raise NotImplementedError("Need to implement this method for correct behaviour")

    def log_info(self, msg):
        if self.logger is not None:
            self.logger.debug(f"[{self.__class__.__name__}] {msg}")

    def log_error(self, msg, error: Exception):
        if self.logger is not None:
            self.logger.debug(f"[{self.__class__.__name__}] {msg}, {error}")

    def get_logger(self):
        return self.logger

    def set_logger(self, logger: logging.Logger):
        self.logger = logger

    def get_client(self):
        return self.client


class TargetCommand(Command):

    def __init__(self, client, guild, target):
        Command.__init__(self, client, guild)

        for i in range(len(target)):
            if type(target[i]) is str and target[i].isnumeric():
                target[i] = int(target[i])

        if all_ in target:
            target = all_
        self.target = self.get_targets(target)  # TEMPLATE METHOD PATTERN

    def __str__(self):
        targets = 'Targets affected: ['
        for target in self.target:
            targets += target.name + ': ' + str(target.id) + ', '
        return Command.__str__(self) + targets[:-2] + ']'

    @abc.abstractmethod
    def get_targets(self, target):
        raise NotImplementedError("Need to implement this method for correct behaviour")


class NullCommand(Command):
    """
    Do nothing command, used for avoid use of
    if command is not None: do something; else: skip
    """

    def __init__(self):
        super().__init__(None, [])

    def __str__(self):
        return 'Null command'

    def run(self):
        pass
