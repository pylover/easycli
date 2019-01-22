import sys
import argparse
import traceback
from os import path


from .command import Command


class Root(Command):
    __completion__ = None

    def __init__(self, argv=None):
        if self.__completion__:
            import argcomplete
            from .completion import Completion
            self.__arguments__.append(Completion)

        super().__init__()

        if self.__completion__:
            argcomplete.autocomplete(self._parser)

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


