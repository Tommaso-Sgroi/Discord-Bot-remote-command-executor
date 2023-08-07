import discord


class InfoGetter:
    def __init__(self, client: discord.client):
        self.client = client

    def get_users(self, guild_id):
        for g in self.client.guilds:
            if g.id == guild_id: return g.members
        return []

    def get_users_names(self, guild_id):
        return [member.name for member in self.get_users(guild_id)]

    def get_guilds(self):
        return self.client.guilds

    def get_guild(self, guild_id):
        for g in self.client.guilds:
            if g.id == guild_id: return g