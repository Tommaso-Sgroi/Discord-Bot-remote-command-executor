"""
This must generate command objects and putting theme into a buffer for
being executing.

It must care about the options:
    --file -> read all instruction from a given path file
    --manual_run -> run the code only when a specific call is find/given
for example (pseudocode):

options:
    --file
expected behaviour:
    command fetched from file and not from console


options:
    --manual_run
expected behaviour:
    command in fetched from console with ainput
    until a specific call is made so it can run
    all the command fetched


options:
    --file --manual_run
expected behaviour:
    command fetched from file and not from console
    until a specific call is read so it can run
    all the command fetched



actually exist 21 command to interpreter... gl
"""
import re
import argparse
import datetime

import discord

from drce.commands.commands_archetypes import Command, NullCommand, all_
from drce.factory.simple_command_factory import SimpleCommandFactory
from drce.reader.reader import Reader
from drce.token.tokens import VoidToken, DistroyToken, StringToken

"""
command structure
{
    action (type) id from guild/guilds id/s
}
Command examples:
    #user type implicit
    ban user user_id from guild_id
    ban user all from guild_id
    ban user all from all

    #same for unban and kick
    #SPECIAL CHARACTER "all"

    delete channel channel_id from guild_id #delete channel
    delete channel all from guilds_id... / all #delete all channels
    delete category all from guild_id

    #make role name = perms from guild_id
    delete role role_id from guild_id
    delete role all from guild_id/guilds_id/all
    reset role role_id from guild_id
    edit role role_id=perms from guild_id
    give role role_id to user_id from guild_id
    add role name=perms from guild_id
    add_and_give role name=perms to user_id from guild_id

    use big_bad_red_button from guild_id
    use defcon #from all implicit
    use silent_guild from guild_id
    use spam from guild_id / guilds_ids / all = "Text..."
"""

from_, to_ = "from", "to"  # from and to keyword for parse where and target
action_, where_, type_, target_ = "action", "where", "type", "target"

user_, role_, channel_, category_, wrapped_ = "user", "role", "channel", "category", "wrapped"  # standard types of
# action_type keyword
defcon, big_bad_red_button, silent_guild, spam = 'defcon', 'big_bad_red_button', 'silent_guild', 'spam'  # wrapped
# standard action_type keyword

ban_, kick_, unban_, delete_, reset_, edit_, add_, use_, give_ \
    = 'ban', 'kick', 'unban', 'delete', 'reset', 'edit', 'add', 'use', 'give'  # actions


class DistroyInterpreter:
    _void_token = VoidToken()
    """Shared void token for not instantiate a new one every time"""

    _string_token = {action_, where_, type_, target_, to_}
    _separator = "--"
    """Separator for strings"""

    def __init__(self, client: discord.Client, reader: Reader):
        parser = argparse.ArgumentParser(description='Distroy command input parser')
        # Optional positional argument
        parser.add_argument(self.add_separator_on_argument(action_), type=str,
                            help='Action to be executed, 1 argument needed')
        parser.add_argument(self.add_separator_on_argument(where_), type=str, nargs='*',
                            help='Guild/Server id where execute the action, one or more arguments needed. "all" means '
                                 + 'al possible guilds')
        parser.add_argument(self.add_separator_on_argument(type_), type=str,
                            help='Type of target on which to apply the action, for example the action --delete can '
                                 + 'affect multiple types: channels, roles. So it is needed for disambiguate the '
                                 + 'targets')
        parser.add_argument(self.add_separator_on_argument(target_), type=str, nargs='*',
                            help='Target id on which perform the action. "all" means all possible targets')
        parser.add_argument(self.add_separator_on_argument(to_), type=str, nargs='*',
                            help='Target on which apply the consequence of a command. Example the give command')

        self.parser = parser
        self.command = ""
        self.reader = reader
        self._command_factory = SimpleCommandFactory(client)

    @staticmethod
    def add_tokens(*tokens):
        DistroyInterpreter._string_token.union(tokens)

    def read(self):
        print_help()
        self.command = self.reader.read()

    def run(self) -> Command:
        command = self.parse_command(self.command)
        return command
        # --action unban --type user --target 287947825587683328 --where 829700927418007553

    def parse_command(self, string) -> Command:
        tokens = re.split('\\s+', string)  # split string at 1-N spaces

        values = dict()
        args = self.parser.parse_args(tokens)

        print(args)
        values[action_] = DistroyToken(args.action) if args.action is not None else VoidToken()
        values[where_] = DistroyToken(args.where) if args.where is not None else VoidToken()
        values[type_] = DistroyToken(args.type) if args.type is not None else VoidToken()
        values[target_] = DistroyToken(args.target) if args.target is not None else VoidToken()
        values[to_] = DistroyToken(args.to) if args.to is not None else VoidToken()

        return self._command_factory.create_command(values)

    # --target 871629604073373706 --action unban --type user --where 829700927418007553

    @staticmethod
    def add_separator_on_argument(arg):
        return DistroyInterpreter._separator + arg


def print_help():
    print(f"--action {[ban_, kick_, unban_, delete_, reset_, edit_, add_, use_, give_]}",
          f"--type {[user_, role_, channel_, category_, wrapped_]}",
          f"--target {['target_id', all_]}",
          f"--where {['guild_id', all_]}",
          f"--to {['user_id', all_]}",
          sep='\n'
          )
