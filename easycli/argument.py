"""A collection command line arguments."""


class Argument:
    """Just a wrapper around :meth:`argparse.ArgumentParser.add_argument`.

    So, except the ``completer`` keyword argument all positional and keywork
    arguments are the same as :meth:`argparse.ArgumentParser.add_argument`.

    :param completer: see `argcomplete <https://argcomplete.readthedocs.io/en\
        /latest/index.html#specifying-completers>`_
    """

    completer = None

    def __init__(self, *a, completer=None, **kw):
        self._args = a
        self._kwargs = kw
        if completer:
            self.completer = completer

    def register(self, parser):
        argument = parser.add_argument(*self._args, **self._kwargs)
        if self.completer:
            argument.completer = self.completer

        return argument


class Mutex(Argument):
    """Mutually exclusive group.

    .. versionadded:: 1.9

    .. code-block::

       class Foo(Root):
           __arguments__ = [
               Mutex(
                   Argument('--bar'),
                   Argument('--baz')
               )
           ]

           ...

    """

    def __init__(self, *args, required=False):
        super().__init__(*args)
        self.required = required

    def register(self, parser):
        group = parser.add_mutually_exclusive_group(required=self.required)
        for a in self._args:
            a.register(group)

        return group
