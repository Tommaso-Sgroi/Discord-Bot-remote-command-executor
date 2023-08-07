import asyncio

import main.distroy


def wait_for_bot_start(drce_bot: main.distroy.DiscordRemoteCommandExecutor):
    """Busy waiting for discord bot starting"""
    import time
    while not drce_bot.can_start:
        drce_bot.logger.debug("waiting for the bot start")
        time.sleep(0.5)


def execute_drce(drce_bot: main.distroy.DiscordRemoteCommandExecutor):
    interpreter = drce_bot.command_interpreter
    executor = drce_bot.command_executor
    wait_for_bot_start(drce_bot)
    while True:
        try:
            interpreter.read()
            command = interpreter.run()

            command.set_logger(drce_bot.logger)

            future: asyncio.Future = executor.run(command)
            result = future.result()  # wait fot the result

            drce_bot.logger.info(f"command executed, result: {result}")

        except Exception as e:
            drce_bot.logger.error("error during execution of drce loop: ", error=e)
