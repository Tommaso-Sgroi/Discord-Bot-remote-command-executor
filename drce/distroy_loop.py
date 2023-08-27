import argparse
import asyncio


from . import distroy
from .exceptions.exception import HelpException


def wait_for_bot_start(drce_bot: distroy.DiscordRemoteCommandExecutor):
    """Busy waiting for discord bot starting"""
    import time
    while not drce_bot.can_start:
        drce_bot.logger.debug("waiting for the bot start")
        time.sleep(0.5)


def execute_drce(drce_bot: distroy.DiscordRemoteCommandExecutor):
    interpreter = drce_bot.command_interpreter
    executor = drce_bot.command_executor

    wait_for_bot_start(drce_bot)
    while True:
        try:
            command_str = interpreter.read()
            command = interpreter.run(command_str)

            future: asyncio.Future = executor.run(command)
            result = future.result()  # wait for the result

            drce_bot.logger.info(f"command executed, result: {result}")

        except argparse.ArgumentError as ae:
            drce_bot.logger.error('argument error: %s', ae)

        except HelpException:  # if the user asked help -> '-h' or '--help' ignore
            continue

        except Exception as e:
            import traceback
            traceback.print_exc()
            drce_bot.logger.error("error during execution of drce loop: %s", e)




