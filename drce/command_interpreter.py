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
import logging
import re
import argparse
from enum import Enum
from typing import List

import discord

from .commands.commands_archetypes import Command, NullCommand, all_
from .exceptions.exception import HelpException
from .factory.simple_command_factory import SimpleCommandFactory
from .reader.reader import Reader
from .token.tokens import VoidToken, DistroyToken, StringToken
from .keywords import ActionType, Action, Argument
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

    def __init__(self, client: discord.Client, reader: Reader, separator='--', string_token: set[str] = None,
                 logger: logging.Logger = None):

        class FixedParser(argparse.ArgumentParser):
            """
            A temporary class used to fix a bug in `argparse.ArgumentParser`.

            This class must not be used outside its intended purpose.

            This bug causes the program to exit even when the 'exit_on_error' flag is set to False. This class
            overrides the `argparse.ArgumentParser.error` method by raising a new `argparse.ArgumentError` with an
            error message, without exiting the program. This behavior is designed specifically for the
            `DistroyInterpreter` class, as exiting on error is not the desired behavior.

            .. note::
                This workaround should only be used in conjunction with the `DistroyInterpreter` class.

            :param status: The exit status code. Defaults to None.
            :type status: int, optional
            :param message: The exit message. Defaults to None.
            :type message: str, optional
            """

            def exit(self, status: int = ..., message: str | None = ...):
                """
                Override of `argparse.ArgumentParser.exit` method.

                In this case, we don't want to terminate the thread from `argparse`.

                :raises argparse.ArgumentError: An exception with the provided exit message.
                """
                pass

            def error(self, message: str):
                """
                Override of `argparse.ArgumentParser.error` method.

                The original method of `argparse.ArgumentParser` invokes `exit` even if the 'exit_on_error' flag is
                set to False. This overridden method raises an `argparse.ArgumentError` with the provided exit
                message instead.

                :raises argparse.ArgumentError: An exception with the provided exit message.
                """
                raise argparse.ArgumentError(message=message, argument=None)

        self._separator = separator
        self._action_args_token = list(Argument)  # TODO keep or remove?
        if string_token is not None:
            self._action_args_token.extend(string_token)

        parser = FixedParser(description='DRCE command input parser', exit_on_error=False, add_help=True)

        # Optional positional argument
        parser.add_argument(self.add_separator_on_argument(Argument.ACTION.value), type=str, default=None,
                            help='Action name to be executed, 1 argument needed')
        parser.add_argument(self.add_separator_on_argument(Argument.WHERE.value), type=str, nargs='*',
                            help='Guild/Server id where execute the action, one or more arguments needed. "all" means '
                                 + 'al possible guilds')
        parser.add_argument(self.add_separator_on_argument(Argument.TYPE.value), type=str, default=None,
                            help='Type of target on which to apply the action, for example the action --delete can '
                                 + 'affect multiple types: channels, roles. So it is needed for disambiguate the '
                                 + 'targets')
        parser.add_argument(self.add_separator_on_argument(Argument.TARGET.value), type=str, nargs='*', default=None,
                            help='Target id on which perform the action. "all" means all possible targets')
        parser.add_argument(self.add_separator_on_argument(Argument.TO.value), type=str, nargs='*', default=None,
                            help='Target on which apply the consequence of a command. Example the give command')

        self.parser = parser
        self.logger = logger
        self.command = ''
        self.reader = reader
        self._command_factory = SimpleCommandFactory(client)

    def add_tokens(self, tokens):
        self._action_args_token.extend(list(tokens))

    def read(self) -> str:
        return self.reader.read()

    def run(self, command_string: str) -> Command:
        command = self.parse_command(command_string)
        return command
        # --action unban --type user --target 287947825587683328 --where 829700927418007553

    def parse_command(self, string) -> Command:
        tokens = re.split('\\s+', string)  # split string at 1-N spaces

        # values = dict()
        args = self.parser.parse_args(tokens)

        # check if the user asked for help. '-h' is default in argparse
        if self.add_separator_on_argument('h') in tokens or \
                '-h' in tokens or \
                self.add_separator_on_argument('help') in tokens:
            raise HelpException()

        if self.logger is not None:
            self.logger.debug('interpreter input args: %s', args)

        # values[action_] = DistroyToken(args.action) if args.action is not None else DistroyInterpreter._void_token
        # values[where_] = DistroyToken(args.where) if args.where is not None else DistroyInterpreter._void_token
        # values[type_] = DistroyToken(args.type) if args.type is not None else DistroyInterpreter._void_token
        # values[target_] = DistroyToken(args.target) if args.target is not None else DistroyInterpreter._void_token
        # values[to_] = DistroyToken(args.to) if args.to is not None else DistroyInterpreter._void_token

        # create a dictionary where the key is a string_token (e.g. {action_, where_, type_, target_, to_})
        # which tells how to create the command to the command factory
        values = {
            key.value: DistroyToken(getattr(args, str(key.value))) if getattr(args, str(key.value)) is not None else
            DistroyInterpreter._void_token
            for key in self._action_args_token
        }

        command: Command = self._command_factory.create_command(values)
        if self.logger is not None:
            command.set_logger(self.logger)
        return command

    # --target 871629604073373706 --action unban --type user --where 829700927418007553

    def print_help(self):
        self.parser.print_help()

    def print_usage(self, file=None):
        self.parser.print_usage(file)

    def add_separator_on_argument(self, arg):
        return self._separator + arg
