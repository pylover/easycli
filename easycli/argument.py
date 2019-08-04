
class Argument:
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

