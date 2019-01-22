
class Argument:
    def __init__(self, *a, **kw):
        self._args = a
        self._kwargs = kw

    def register(self, parser):
        return parser.add_argument(*self._args, **self._kwargs)


