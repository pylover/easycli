
class Argument:
    def __init__(self, *a, **kw):
        self._args = a
        self._kwargs = kw

    def register(self, parser):
        from pudb import set_trace; set_trace()
        return parser.add_argument(*self._args, **self._kwargs)

