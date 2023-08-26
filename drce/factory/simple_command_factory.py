from typing import Dict

from ..commands.wrapped_commands import *
from ..token.tokens import StringToken, DistroyToken
from ..keywords import *
from ..exceptions.exception import MissingArgumentException


def _check_missing_args(handle_action):
    """check if all arguments have a not null or empty value assigned"""
    def wrap_check_args(*args, **kwargs):
        if None in args or None in kwargs.values() or [] in args or [] in kwargs.values():
            raise MissingArgumentException('one or more fields values are missing')
        return handle_action(*args, **kwargs)

    return wrap_check_args


class DistroyFactory(abc.ABC):

    @abc.abstractmethod
    def create_command(self, string_token: StringToken) -> Command:
        pass


class SimpleCommandFactory(DistroyFactory):

    def __init__(self, client: discord.Client):
        self.client = client

    def create_command(self, token_value: Dict[str, DistroyToken]) -> Command:
        action = token_value.get(Argument.ACTION.value).get_token()
        action_type = token_value.get(Argument.TYPE.value).get_token()
        target_object = token_value.get(Argument.TARGET.value).get_token()
        where = token_value.get(Argument.WHERE.value).get_token()
        to = token_value.get(Argument.TO.value).get_token()

        # Use the match statement to handle different cases based on action_type
        match action_type:
            case ActionType.USER.value:
                command = self.handle_user(action, where, target_object)
            case ActionType.ROLE.value:
                command = self.handle_role(action, where, to, target_object)
            case ActionType.CHANNEL.value:
                command = self.handle_channel(action, where, target_object)
            case ActionType.WRAPPED.value:
                command = self.handle_wrapped(action, where)
            case _:
                raise Exception(f"Cannot recognize action type: {action_type}")

        return command

    @_check_missing_args
    def handle_user(self, action, where, target_object) -> UserCommand:
        match action:
            case Action.BAN.value:
                return BanCommand(self.client, where, target_object)
            case Action.KICK.value:
                return KickCommand(self.client, where, target_object)
            case Action.UNBAN.value:
                return UnbanCommand(self.client, where, target_object)
            case _:
                self.raise_action_exception(action)

    @_check_missing_args
    def handle_role(self, action, where, to, target_object) -> Command:
        # role_id = perms
        target, perms = target_object, None
        match action:
            case Action.DELETE.value:
                return DeleteRoleCommand(self.client, where, target)

            case Action.RESET.value:
                return ResetRoleCommand(self.client, where, target)

            case Action.EDIT.value:
                if type(target_object[0]) is str:
                    target_perms = target_object[0].split('=')
                    target = target_perms[0]
                    perms = target_perms.pop()
                return EditRoleCommand(self.client, where, target, perms)

            case Action.ADD.value:
                if type(target_object[0]) is str:
                    target_perms = target_object[0].split('=')
                    target = target_perms[0]
                    perms = target_perms.pop()
                return AddRoleCommand(self.client, where, target, perms)  # name=target because it has no target at all

            case Action.GIVE.value:
                return GiveRoleCommand(self.client, where, target, to)

            case _:
                self.raise_action_exception(action)

    @_check_missing_args
    def handle_channel(self, action, where, target_object) -> TargetCommand:
        if action == Action.DELETE.value:
            return DeleteChannelCommand(self.client, where, target_object)
        self.raise_action_exception(action)

    @_check_missing_args
    def handle_wrapped(self, action, where) -> Command:

        match action:
            case Action.RED_BUTTON.value:
                return BigBadRedButton(self.client, where)

            case Action.DEFCON.value:
                return Defcon(self.client)

            case Action.SILENT_GUILD.value:
                return SilentGuild(self.client, where)

            case Action.SPAM.value:
                return Spam(self.client, where, "THIS IS A TESTING MESSAGE I HAVE TO CHANGE IT!!!!")

            case _:
                self.raise_action_exception(action)

    def raise_action_exception(self, action):
        raise Exception(f'Cannot recognize "action":{action}')
