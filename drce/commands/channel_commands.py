from ..commands.commands_archetypes import *


class DeleteChannelCommand(TargetCommand):

    def __init__(self, client, guild, target):
        TargetCommand.__init__(self, client, guild, target)

    def __str__(self):
        return TargetCommand.__str__(self)

    def get_targets(self, target):
        if target == all_:
            return [channel for guild in self.guild for channel in guild.channels]
        channels = []
        for guild in self.guild:
            for t in target:
                c = guild.get_channel(t)
                if c is not None:
                    channels.append(c)
        return channels

    # @Command.log_exception
    async def run(self):
        for channel in self.target:
            try:
                await channel.delete()
                self.log_info(f"deleted {channel} successfully in guild {channel.guild}")
            except Exception as e:
                self.log_error(f"error deleting channel {channel}", e)

# class DeleteAllChannelsCommand(DeleteChannelCommand):
#     def __init__(self, guilds):
#         if type(guilds) == list:
#             self.channels = []
#             for g in guilds:
#                 Command.__init__(self, g)
#                 for channel in self.guild.channels:
#                     self.channels.append(channel)
#         else:
#             TargetCommand.__init__(self, guilds, None)
#             self.channels = self.guild.channels
#         #print(self.channels)
#
#     async def run(self):
#         for channel in self.channels:
#             self.channel = channel
#             await super().run()


# class DeleteAllCategoriesCommand(Command):
#     def __init__(self, guild):
#         Command.__init__(self, guild)
#
#     async def run(self):
#         for c in self.guild.categories:
#             await c.delete()

# class AddChannelCommand(TargetCommand):
#     def __init__(self, guild, name, category, channel_type: ChannelType): #target = la categoria
#         self.guild = guild
#         self.category = category
#         self.channel_type = channel_type
#         self.name = name
#
#     async def run(self):
#         if self.channel_type == ChannelType.text:
#             await create_text_channel(self.name)
#         elif self.channel_type == ChannelType.news:
#             pass
#         elif self.channel_type == ChannelType.store:
#             pass
#         elif self.channel_type == ChannelType.group:
#             pass
#         elif self.channel_type == ChannelType.voice:
#             pass
