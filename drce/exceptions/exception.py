class HelpException(Exception):
    pass


class MissingArgumentException(Exception):
    """Exception raised for missing required arguments."""

    def __init__(self, message="one or more fields values are missing"):
        self.message = message
        super().__init__(self.message)
