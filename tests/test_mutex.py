from easycli import Root, Argument, Mutex

from bddcli import stdout, status, stderr, Application, Given, when


class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __arguments__ = [
        Mutex(
            Argument('--bar', action='store_true'),
            Argument('--baz', action='store_true'),
        )
    ]

    def __call__(self, args):
        print('foo done')


EXPECTED_HELP = '''usage: foo [-h]

Foo Help

optional arguments:
  -h, --help  show this help message and exit
'''


EXPECTED_USAGE = '''\
usage: foo [-h] [--bar | --baz]
foo: error: argument --baz: not allowed with argument --bar
'''


def test_mutex():
    app = Application('foo', 'tests.test_mutex:Foo.quickstart')
    with Given(app):
        assert stderr == ''
        assert stdout == 'foo done\n'
        assert status == 0

        when(['--bar'])
        assert status == 0
        assert stderr == ''
        assert stdout == 'foo done\n'

        when(['--baz'])
        assert status == 0
        assert stderr == ''
        assert stdout == 'foo done\n'

        when(['--bar --baz'])
        assert status == 2
        assert stderr == EXPECTED_USAGE
        assert stdout == ''


if __name__ == '__main__':
    Foo().main(['--bar', '--baz'])
