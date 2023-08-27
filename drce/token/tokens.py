class DistroyToken:
    """
    Represent a Distroy token, used to provide the appropriate input to a Command or TargetCommand class.

    This token can represent the following inputs:
    - 'all' guilds
    - 'all' targets
    - Numeric guild
    - Numeric target
    """

    def __init__(self, token):
        """Can be string or list[str]"""
        if token is str:
            self.token = token.lower()
        else:
            self.token = token

    def __eq__(self, other):
        # print(other)
        if type(other) is str:
            return self.get_token() == other
        elif isinstance(other, DistroyToken):
            return self.get_token() == other.get_token()

    def __str__(self):
        return self.get_token()

    def get_token(self):
        """
        :return: int token if token is numeric else return token itself
        """
        if self.token is str and self.token.isnumeric():
            return int(self.token)
        return self.token


class VoidToken(DistroyToken):
    """
    Just a void token for avoid checks
    """

    def __init__(self):
        DistroyToken.__init__(self, '')
        self.token = None

    def get_token(self):
        return self.token


class StringToken:

    def __init__(self, **tokens):
        self.string_token = tokens

    def __iter__(self):
        return self.string_token.__iter__()

    def add_string_token(self, **tokens):
        self.string_token.update(tokens)

    def get(self, s):
        return self.string_token.get(s)
