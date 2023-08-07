import discord

from drce.command_executor import DistroyExecutor
from drce.command_interpreter import DistroyInterpreter
from drce.reader.reader import Reader


def new_command_executor(client: discord.Client):
    return DistroyExecutor(client)


def new_command_interpreter(client: discord.Client, reader: Reader):
    return DistroyInterpreter(client, reader)
