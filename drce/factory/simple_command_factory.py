from drce.commands.wrapped_commands import *
from drce.token.tokens import StringToken


class DistroyFactory(abc.ABC):

    @abc.abstractmethod
    def create_command(self, string_token: StringToken) -> Command:
        pass


class SimpleCommandFactory(DistroyFactory):

    def __init__(self, client: discord.Client):
        self.client = client

    def create_command(self, string_token: dict) -> Command:
        action = string_token.get('action').get_token()
        action_type = string_token.get('type').get_token()
        target_object = string_token.get('target').get_token()
        where = string_token.get('where').get_token()
        to = string_token.get('to').get_token()

        command: Command = NullCommand()

        # Use the match statement to handle different cases based on action_type
        match action_type:
            case 'user':
                command = self.handle_user(action, where, target_object)
            case 'role':
                command = self.handle_role(action, where, to, target_object)
            case 'channel':
                command = self.handle_channel(action, where, target_object)
            case 'wrapped':
                command = self.handle_wrapped(action, where)
            case _:
                raise Exception(f"Cannot recognize 'type': {action_type}")

        return command

    def handle_user(self, action, where, target_object) -> UserCommand:

        self.check_missing_target_or_where_exception(target_object, where)
        match action:
            case 'ban':
                return BanCommand(self.client, where, target_object)
            case 'kick':
                return KickCommand(self.client, where, target_object)
            case 'unban':
                return UnbanCommand(self.client, where, target_object)
            case _:
                self.raise_action_exception(action)

    def handle_role(self, action, where, to, target_object) -> Command:
        self.check_missing_target_or_where_exception(target_object, where)

        # role_id = perms
        target, perms = target_object, None
        match action:
            case 'delete':
                return DeleteRoleCommand(self.client, where, target)

            case 'reset':
                return ResetRoleCommand(self.client, where, target)

            case 'edit':
                if type(target_object[0]) is str:
                    target_perms = target_object[0].split('=')
                    target = target_perms[0]
                    perms = target_perms.pop()
                return EditRoleCommand(self.client, where, target, perms)

            case 'add':
                if type(target_object[0]) is str:
                    target_perms = target_object[0].split('=')
                    target = target_perms[0]
                    perms = target_perms.pop()
                return AddRoleCommand(self.client, where, target, perms)  # name=target because it has no target at all

            case 'give':
                return GiveRoleCommand(self.client, where, target, to)

            case _:
                self.raise_action_exception(action)

    def handle_channel(self, action, where, target_object) -> TargetCommand:

        self.check_missing_target_or_where_exception(target_object, where)

        if action == 'delete':
            return DeleteChannelCommand(self.client, where, target_object)

        self.raise_action_exception(action)

    def handle_wrapped(self, action, where) -> Command:

        match action:
            case 'bbrb':
                self.check_missing_target_or_where_exception(-1, where)
                return BigBadRedButton(self.client, where)

            case 'defcon':
                return Defcon(self.client)

            case 'silent_guild':
                self.check_missing_target_or_where_exception(-1, where)
                return SilentGuild(self.client, where)

            case 'spam':
                self.check_missing_target_or_where_exception(-1, where)
                return Spam(self.client, where, "THIS IS A TESTING MESSAGE I HAVE TO CHANGE IT!!!!")

            case _: self.raise_action_exception(action)

    def raise_action_exception(self, action):
        raise Exception(f'Cannot recognize "action":{action}')

    def check_missing_target_or_where_exception(self, target_object, where):
        if target_object is None or where is None:
            raise Exception('"target" or "where" field are missing')
