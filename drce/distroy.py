from .reader.console_reader import CommandConsoleReader
from .reader.file_reader import CommandScriptFileReader
from .utils import *


class DiscordRemoteCommandExecutor:
    """
    This class initializes a DiscordRemoteCommandExecutor object by instantiating essential attributes such as the
    discord client, options, and logger. It also creates a command interpreter and executor to handle owner's commands.

    :param client: The discord client instance.
    :param options: The options for the command executor.
    :param logger: The logger for logging events and information.
    """

    def __init__(self, client, options, logger):
        """
        Make a DiscordRemoteCommandExecutor object instantiating:
            - command interpreter
            - command executor
            - reader
        """
        self.client = client  # discord.client
        if self.client is not None and isinstance(self.client, discord.Client):
            self.inject_client_commands()
        else:
            raise AttributeError()

        self.options = options
        self.logger = logger

        # read commands from cmd or file if a path wasn't given at start
        reader = CommandConsoleReader() if self.options.script_file == '' or self.options.script_file is None \
            else CommandScriptFileReader(self.options.script_file)  # read commands from file if a path was givens

        self.command_interpreter = new_command_interpreter(self.client, reader, logger)
        self.command_executor = new_command_executor(self.client)

        self.can_start = False  # true if the bot has started and the user can start to write and execute commands

    def inject_client_commands(self):
        """
        Manually injects a wrapper into your Bot's 'on_ready' function that sets the 'can_start' attribute to True.
        This allows the DiscordRemoteCommandExecutor to start. It functions similarly to a decorator but does not create
        a direct dependency between the client and this object.

        The injected wrapper modifies the behavior of the 'on_ready' method, ensuring that the 'can_start' attribute is
        set to True upon successful completion.

        :Usage:
            This function, is called during the instantiation of this class.

        :Example:

        .. code-block:: python

            bot = YourBot(command_prefix='$', ...)
            drce = new_drce(bot, ...)

            # .......
            # inside the __init__
            self.client = client  # discord.client
            if self.client is not None and isinstance(self.client, discord.Client):
                self.inject_client_commands()

        :Note:
            The injected wrapper enhances the 'on_ready' behavior without directly modifying the Bot class.

        """

        def inject_on_ready(on_ready_func):
            async def on_ready_wrapper(*args, **kwargs):
                res = await on_ready_func(*args, **kwargs)
                self.can_start = True
                return res

            return on_ready_wrapper

        if not hasattr(self.client, 'on_ready'):
            # Create a void on_ready method
            async def empty_on_ready(*_, **__):
                pass  # Empty async method

            # self.client.on_ready = empty_on_ready
            setattr(self.client, 'on_ready', empty_on_ready())  # Create an empty method

        # Inject the client.on_ready method with the wrapped one
        # self.client.on_ready = inject_on_ready(self.client.on_ready)
        setattr(self.client, 'on_ready', inject_on_ready(getattr(self.client, 'on_ready')))

    def set_options(self, options):
        self.options = options

    def set_client(self, client: discord.Client):
        self.client = client
        self.inject_client_commands()

    def run_client(self):
        self.client.run(self.options.token)

