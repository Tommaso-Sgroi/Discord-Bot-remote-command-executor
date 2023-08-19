import discord
from discord.ext import commands

COMMAND_PREFIX = '-'


def new_client():
    intents = discord.Intents.all()
    return YourBot(command_prefix=COMMAND_PREFIX, intents=intents)


class YourBot(commands.Bot):

    async def on_ready(self):
        print(f'We HAVE logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send(f'Hello <@{message.author.id}>!')

    async def on_member_join(self, member: discord.Member) -> None:
        welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if welcome_channel is None:
            welcome_channel = await member.guild.create_text_channel('welcome')
            await member.guild.create_voice_channel('welcome')
        await welcome_channel.send(f"Hello {member.mention} !")
