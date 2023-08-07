import asyncio

import discord


class DistroyExecutor:

    def __init__(self, options=None):
        self.options = options
        self.client = None  # discord.Client
        self.command_list = list()

    def set_client(self, client: discord.Client):
        self.client = client

    def run(self, command):
        return self.between_callback(command)

    def between_callback(self, command):
        """This function is needed for avoid the use of 'async' in thread method run"""
        # now we need to run the command coroutine in the client original loop! 'troy_bot.client.loop'
        send_fut = asyncio.run_coroutine_threadsafe(
            DistroyExecutor.execute(command),
            self.client.loop)
        return send_fut

    @staticmethod
    async def execute(command):
        await command.run()
