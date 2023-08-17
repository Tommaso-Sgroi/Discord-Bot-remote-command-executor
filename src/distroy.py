import discord

from drce.reader.console_reader import CommandConsoleReader
from drce.reader.file_reader import CommandScriptFileReader
from drce.utils import *
from drce.reader import *

"""
This module is only for share troy_bot global variable
among other modules
"""


class DiscordRemoteCommandExecutor:
    """
    Object that represent the bot with his options
    """

    def __init__(self, **kwargs):
        """
        Make a DiscordRemoteCommandExecutor object instantiating:
            - @discord.Intents
            - command prefix
            - logger
            - discord client
            - command interpreter
            - command executor
            ecc
        """
        self.client = kwargs['client']  # discord.client
        if self.client is not None and isinstance(self.client, discord.Client):
            self.inject_client_commands()
        else:
            raise AttributeError()

        self.options = kwargs['options']
        self.logger = kwargs['logger']

        # read commands from cmd or file if a path wasn't given at start
        reader = CommandConsoleReader() if self.options.script_file == '' or self.options.script_file is None \
            else CommandScriptFileReader(self.options.script_file)  # read commands from file if a path was givens

        self.command_interpreter = new_command_interpreter(self.client, reader)
        self.command_executor = new_command_executor(self.client)

        self.can_start = False  # true if the bot has started and the user can start to write and execute commands

    def set_options(self, options):
        self.options = options

    def set_client(self, client: discord.Client):
        self.client = client

    def run_client(self):
        self.client.run(self.options.token)

    def inject_client_commands(self):
        client = self.client

        @client.event
        async def on_ready():
            self.can_start = True
            print(f'We have logged in as {client.user}')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            if message.content.startswith('$hello'):
                await message.channel.send(f'Hello <@{message.author.id}>!')

        @client.event
        async def on_member_join(member: discord.Member):
            welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
            if welcome_channel is None:
                welcome_channel = await member.guild.create_text_channel('welcome')
                await member.guild.create_voice_channel('welcome')
            await welcome_channel.send(f"Hello {member.mention} !")

        return

    def get_all_guilds_ids(self):
        """
        :return: a list with all guilds ids
        """
        return [guild.id for guild in self.client.guilds]
