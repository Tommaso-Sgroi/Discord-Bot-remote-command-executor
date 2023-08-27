class Configuration:

    def __init__(self, *, script_file, log_file, token):
        self.script_file = script_file
        self.log_file = log_file if log_file != "" else None
        self.token = token

    def __str__(self):
        return f"Configuration(script_file='{self.script_file}', log_file='{self.log_file}', token='{self.token}')"


def fetch_config():
    import argparse

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')

    # Required positional argument
    parser.add_argument('--token', type=str,
                        help='Discord bot token, you can find it in your bot application on discord developer portal')

    # Optional positional argument
    parser.add_argument('--script_file', type=str, nargs='?',
                        help='A required integer positional argument')

    # Optional positional argument
    parser.add_argument('--log_file', type=str, nargs='?',
                        help='An optional integer positional argument')
    args = parser.parse_args()
    if not args.token or args.token == '':
        import sys
        parser.error("You must put your bot token --token xxxxx")
        sys.exit(1)

    return Configuration(script_file=args.script_file, log_file=args.log_file, token=args.token)
