import discord


def new_client():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    # @client.event
    # async def on_ready():
    #     print(f'We have logged in as {client.user}')
    #
    # @client.event
    # async def on_message(message):
    #     if message.author == client.user:
    #         return
    #
    #     if message.content.startswith('$hello'):
    #         await message.channel.send(f'Hello <@{message.author.id}>!')
    #
    # @client.event
    # async def on_member_join(member: discord.Member):
    #     welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
    #     if welcome_channel is None:
    #         welcome_channel = await member.guild.create_text_channel('welcome')
    #         await member.guild.create_voice_channel('welcome')
    #     await welcome_channel.send(f"Hello {member.mention} !")

    return client
