import logging
import threading

import discord

from main.client import new_client
from main.distroy import DiscordRemoteCommandExecutor
from main.distroy_loop import execute_drce
from main.thread_interrupt import ThreadInterrupt


LOGGER_NAME = "distroy_logger"


# def signal_handler(sig, _):
#     # Raise the custom exception to interrupt the threads
#     logging.info(f"received sig {sig}, all threads will be interrupted")
#     raise ThreadInterrupt


def new_drce(client: discord.Client, options):
    import main.utils
    return DiscordRemoteCommandExecutor(
        # drce_executor=drce.utils.new_command_executor(),
        # drce_interpreter=drce.utils.new_command_interpreter(),
        options=options,
        client=client,
        logger=main.utils.create_custom_logger(LOGGER_NAME, options.log_file),
    )


def start(options):

    client = new_client()
    drce = new_drce(client, options)

    drce_thread = threading.Thread(target=execute_drce, args=(drce,))

    # Start the threads
    drce.logger.info("DRCE starting...")
    drce_thread.start()

    drce.logger.info("your bot is starting...")
    drce.run_client()

    # try:
    #     # Wait for both threads to finish
    #     drce_thread.join()
    # except ThreadInterrupt:
    #     # If a signal is received, interrupt the threads and wait for them to finish
    #     drce_thread.join()

    logging.info("exiting")
