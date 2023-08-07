from drce.commands.commands_archetypes import *


class UserCommand(TargetCommand):

    def __init__(self, client, guild, target, action_type=''):
        """
        :param guild: guild id
        :param target: target id
        for some reason the "reason" cannot be specified
        """
        TargetCommand.__init__(self, client, guild, target)
        self.action_type = action_type

    def __str__(self):
        targets = 'Targets affected:\n'
        for tup in self.target:
            for user in tup[1]:
                targets += user.name + ': ' + str(user.id) + '\n'
        return Command.__str__(self) + targets

    def get_targets(self, target):
        users = []
        if target == all_:
            for guild in self.guild:
                users.append((guild, guild.members))  # tuple (Guild, MembersList)
        else:
            for guild in self.guild:
                for t in target:
                    user = guild.get_member(t)
                    if user is not None:
                        users.append((guild, [user]))  # tuple (Guild, MembersList)
        return users

    async def run(self):
        for guild_members in self.target:
            guild = guild_members[0]
            users = guild_members[1]
            for user in users:
                await self.action(user, guild)  # TEMPLATE METHOD PATTERN

    @abc.abstractmethod
    def get_action(self):
        raise NotImplementedError("Need to implement this method for correct behaviour")

    @abc.abstractmethod
    async def action(self, user, guild):
        raise NotImplementedError("Need to implement this method for correct behaviour")


class BanCommand(UserCommand):
    """
    Command that ban a member from a guild
    """

    def __init__(self, client, guild, target):
        """
        :param guild: guild id
        :param target: target id
        for some reason the "reason" cannot be specified
        """
        UserCommand.__init__(self, client, guild, target, 'banning')

    def get_action(self):
        return "BAN"

    async def action(self, user, guild):
        try:
            await guild.ban(user)
            self.log_info(f'banned user "{user}" in guild {guild}')
        except Exception as e:
            self.log_error(f'error banning user "{user}" in guild "{guild}": ', e)


class UnbanCommand(UserCommand):

    def __init__(self, client, guild, target):
        """
        :param guild: guild obj
        :param target: target name#number
        for some reason the "reason" cannot be specified
        """
        UserCommand.__init__(self, client, guild, target, 'unbanning')

    def __str__(self):
        targets = 'Targets affected: ['
        for target in self.target:
            targets += target + ", "
        return Command.__str__(self) + targets[:-2] + "]"

    def get_targets(self, target):
        return target

    async def run(self):
        # extract all the targets
        target = self.target
        self.target = []
        for guild in self.guild:
            if target == all_:
                self.target.append((guild, [ban_entry.user for ban_entry in await guild.bans()]))
            else:
                banned_users = await guild.bans()
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if user.id in target:
                        self.target.append((guild, [user]))
        # finally unban all the targets
        await super().run()

    async def action(self, user, guild):
        try:
            await guild.unban(user)
            self.log_info(f'unbanned user "{user}" in guild "{guild}"')
        except Exception as e:
            self.log_error(f'cannot unban "{user}" in guild "{guild}": ', e)

    def get_action(self):
        return "UNBAN"


class KickCommand(UserCommand):

    def __init__(self, client, guild, target):
        """
            :param guild: guild id
            :param target: target id
            for some reason the "reason" cannot be specified
            """
        UserCommand.__init__(self, client, guild, target, 'kicking')

    async def action(self, user, guild):
        try:
            await guild.kick(user)
            self.log_info(f'kicked user "{user}" from guild "{guild}"')
        except Exception as e:
            self.log_error(f'cannot kick user "{user}" from guild "{guild}": ', e)

    def get_action(self):
        return "KICK"
