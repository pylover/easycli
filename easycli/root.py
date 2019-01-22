import sys
import argparse
import traceback
from os import path

from .command import Command


class Root(Command):

    def __init__(self, argv=None):
        super().__init__()
        self.launch(argv)

    def launch(self, argv):
        args = self._parser.parse_args(argv)
        try:
            if hasattr(args, 'func'):
                exitcode = args.func(args)
            else:
                exitcode = self(args)
        except:
            traceback.print_exc()
            exitcode = 1

        sys.exit(exitcode or 0)

    @classmethod
    def _create_parser(self):
        return argparse.ArgumentParser(
            prog=path.basename(sys.argv[0]),
            description=self.__help__
        )


