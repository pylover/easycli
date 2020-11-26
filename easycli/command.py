from abc import ABCMeta

from .argument import Argument


class Command(metaclass=ABCMeta):
    """Abstract base class for all commands."""

    #: List of both :class:`.Command` class or instance of :class:`.Argument`
    __arguments__ = []

    #: str, command name
    __command__ = None

    #: List of aliases for the :attr:`.__command__`
    __aliases__ = None

    #: Help message to show when -h/--help
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
        """Execute the command.

        This method should be implemented in the child class to do what the
        command does.

        :param args: What :meth:`argparse.ArgumentParser.parse_args` returns.
        """
        if self._parser:
            self._parser.print_help()


class SubCommand(Command):
    """Base class for sub commands.

    .. code-block:: bash

       root subcommand subsubcommand

    For example, in ``git push ..`` scenario ``push`` is a sub command.

    Users must inherit this class and configure the sub class to create new
    shell sub command behavior.

    .. code-block::

       from easycli import SubCommand, Root


       class Push(SubCommand):
           __command__ = 'push'
           __aliases__ = ['p', 'pu']
           __arguments__ = [
               ...
           ]


       class Git(Root):
           ...
           __arguments__ = [
               Push,
               ...
           ]
    """

    def __init__(self, subparsers):
        self._parent_subparsers = subparsers
        super().__init__()

    def _create_parser(self):
        assert self.__command__, 'Please provide a name for your command' \
            ' using __command__ class attribute'

        kw = dict(
            help=self.__help__,
        )
        if self.__aliases__:
            kw['aliases'] = self.__aliases__

        parser = self._parent_subparsers.add_parser(self.__command__, **kw)
        parser.set_defaults(func=self)
        return parser
