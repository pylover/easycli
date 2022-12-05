from easycli import Root, SubCommand, Argument

from bddcli import stdout, status, stderr, Application, Given, when


class Bar(SubCommand):
    __help__ = 'Bar help'
    __command__ = 'bar'
    __aliases__ = ['b', 'ba']
    __arguments__ = [
        Argument('-b', '--baz', action='store_true')
    ]

    def __call__(self, args):
        print('Bar done:', args.baz)
        if args.baz:
            return 1


class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __arguments__ = [Bar]


def test_subcommand():
    app = Application('foo', 'tests.test_subcommand:Foo.quickstart')
    with Given(app):
        assert status == 0

        when(['-h'])
        assert status == 0
        assert stderr == ''

        when(['bar'])
        assert stderr == ''
        assert stdout == 'Bar done: False\n'
        assert status == 0

        when(['ba'])
        assert stderr == ''
        assert stdout == 'Bar done: False\n'
        assert status == 0

        when(['b'])
        assert stderr == ''
        assert stdout == 'Bar done: False\n'
        assert status == 0

        when(['bar', '--baz'])
        assert stderr == ''
        assert stdout == 'Bar done: True\n'
        assert status == 1


if __name__ == '__main__':
    Foo().main(['-h'])
