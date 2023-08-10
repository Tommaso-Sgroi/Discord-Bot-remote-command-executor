import sys

from main.distroy import DiscordRemoteCommandExecutor
import drce.utils
import logging

LOGGER_NAME = "distroy_logger"


def create_custom_logger(logger_name, log_file=None):
    # Create a new logger with the specified name
    logger = logging.getLogger(logger_name)

    # Set the logging level for the logger (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.DEBUG)

    # Create a handler to determine where the log messages should be sent
    if log_file is None:
        handler = logging.StreamHandler(sys.stdout)  # Log messages will be sent to the console
    else:
        # Alternatively, you can use a FileHandler to send log messages to a file:
        handler = logging.FileHandler(log_file, encoding='utf-8', mode='a')

    # Create a formatter to format log messages
    formatter = logging.Formatter("[%(asctime)s] [%(threadName)s] [%(levelname)s] %(message)s")

    # Set the formatter for the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


# def new_troy_bot(options):
#     troy_bot = DiscordRemoteCommandExecutor()
#     troy_bot.command_interpreter = drce.utils.new_command_interpreter()
#     troy_bot.command_executor = drce.utils.new_command_executor()
#
#     troy_bot.logger = create_custom_logger(LOGGER_NAME, options.log_file)
#
#     return troy_bot
