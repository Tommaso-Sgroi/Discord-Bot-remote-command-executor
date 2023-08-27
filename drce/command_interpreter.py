import logging
import re
import argparse

import discord

from .commands.commands_archetypes import Command
from .exceptions.exception import HelpException
from .factory.simple_command_factory import SimpleCommandFactory
from .reader.reader import Reader
from .token.tokens import VoidToken, DistroyToken
from .keywords import Argument


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
