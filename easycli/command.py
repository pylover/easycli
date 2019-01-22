
from .argument import Argument


class Command:
    __arguments__ = []
    __command__ = None
    __help__ = None

    def __init__(self):
        self._parser = self._create_parser()

        _subcommands = []
        for a in self.__arguments__:
            if isinstance(a, Argument):
                a.register(self._parser)
            else:
                _subcommands.append(a)

        if _subcommands:
            self._subparsers = self._parser.add_subparsers(
                title='Sub commands',
                dest='command'
            )

            for p in _subcommands:
                p(self._subparsers)

    def _create_parser(self):
        raise NotImplementedError()

    def __call__(self, args):
        if self._parser:
            self._parser.print_help()


class SubCommand(Command):
    def __init__(self, subparsers):
        self._parent_subparsers = subparsers
        super().__init__()

    def _create_parser(self):
        assert self.__command__, 'Please provide a name for your command' \
            ' using __command__ class attribute'


        parser = self._parent_subparsers.add_parser(
            self.__command__,
            help=self.__help__
        )
        parser.set_defaults(func=self)
        return parser

