import sys
import argparse
import traceback
from os import path

from .command import Command


class Root(Command):
    __completion__ = None

    def __init__(self, argv=None):
        if self.__completion__:
            from .completion import Completion
            self.__arguments__.append(Completion)

        super().__init__()

    @classmethod
    def _create_parser(self):
        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        return argparse.ArgumentParser(
            prog=path.basename(sys.argv[0]),
            description=self.__help__
        )

    def main(self, argv=None):
        if self.__completion__:
            import argcomplete
            argcomplete.autocomplete(self._parser)

        argv = argv or sys.argv
        args = self._parser.parse_args(argv)

        return args.func(args) if hasattr(args, 'func') else self(args)

