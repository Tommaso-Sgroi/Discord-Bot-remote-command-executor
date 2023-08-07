class Options:

    def __init__(self, **kwargv):
        self.script_file = kwargv["script_file"]
        self.log_file = kwargv["log_file"] if kwargv["log_file"] != "" else None
        self.token = kwargv['token']

    def __str__(self) -> str:
        return "[script file]" + str(self.script_file) + "; " + "[output file]" + str(self.log_file)


def fetch_options():
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
        parser.error("You must put your bot token --token xxxxx")
        exit(1)

    return Options(script_file=args.script_file, log_file=args.log_file, token=args.token)
