import sys
import argparse
from os import path

from .command import Command


class Root(Command):
    """base class for the CLI entry point.

    .. code-block::

       import sys

       from easycli import Root, ...


       class Git(Root):
           __help__ = 'git help message'
           __completion__ = True
           __arguments__ = [
               Pull,
               Push,
               Commit,
               ...
           ]

       if __name__ == '__main__':
           sys.exit(Git.quickstart())

    """

    __completion__ = None
    """If True, a completion sub-command with two subsub-commands: install and
    uninstall will be added to ``self.__arguments__`` collection.
    """

    def __init__(self):
        if self.__completion__:
            from .completion import Completion
            self.__arguments__.append(Completion)

        super().__init__()

        if self.__completion__:
            import argcomplete
            argcomplete.autocomplete(self._parser)

    @classmethod
    def _create_parser(self):
        return argparse.ArgumentParser(
            prog=path.basename(self.__command__ or sys.argv[0]),
            description=self.__help__
        )

    def _execute_subcommand(self, args):
        return args.func(args)

    def main(self, argv=None):
        """Call this function as the main entry point for your cli application.

        :param argv: If not given, :attr:`sys.argv` will be used.
        :return: exit status
        """
        # Parse Argument
        args = self._parser.parse_args(argv)

        if hasattr(args, 'func'):
            status = self._execute_subcommand(args)
        else:
            status = self(args)

        return status or 0

    @classmethod
    def quickstart(cls, argv=None):
        """Shorthand for ``Root().main()``."""
        return cls().main(argv)
