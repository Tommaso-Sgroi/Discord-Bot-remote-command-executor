# import discord
#
#
# async def on_ready():
#     print(f'We have logged in as {client.user}')
#
#
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send(f'Hello <@{message.author.id}>!')
#
#
# async def on_member_join(member: discord.Member):
#     welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
#     if welcome_channel is None:
#         welcome_channel = await member.guild.create_text_channel('welcome')
#         await member.guild.create_voice_channel('welcome')
#     await welcome_channel.send(f"Hello {member.mention} !")